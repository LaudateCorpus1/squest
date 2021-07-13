from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils.safestring import mark_safe
from graphviz import Digraph
from django.template import Template, Context
from django.template.loader import get_template
from resource_tracker.models import ResourceGroup, ResourcePool
from django.urls import reverse

COLORS = {'consumer': '#28a745', 'provider': '#dc3545', 'resource_pool': '#6ddbbb', 'resource_group': '#7fb4d3',
          'available': '#ffc107'}
COLORS["bg-green"] = "#28a745"
COLORS["bg-yellow"] = "#ffc107"
COLORS["bg-red"] = "#dc3545"


@user_passes_test(lambda u: u.is_superuser)
def resource_tracker_graph(request):
    dot = Digraph(comment='Graph')
    dot.attr(bgcolor='#ffffff00')
    dot.name = 'Resource Tracker Graph'
    dot.attr('node', shape='plaintext')

    for resource_pool in ResourcePool.objects.filter():
        dot.node(resource_pool.name, label=create_resource_pool_svg(resource_pool))
    for resource_group in ResourceGroup.objects.filter():

        dot.node(resource_group.name, label=create_resource_group_svg(resource_group))
        for attribute in resource_group.attribute_definitions.filter():
            rg = f"{resource_group.name}:{attribute.name}"
            if attribute.consume_from:
                dot.edge(f"{attribute.consume_from.resource_pool.name}:{attribute.consume_from.name}", rg,
                         color=COLORS['provider'])
            if attribute.produce_for:
                dot.edge(rg, f"{attribute.produce_for.resource_pool.name}:{attribute.produce_for.name}",
                         color=COLORS['consumer'])

    dot.format = 'svg'
    svg = mark_safe(dot.pipe().decode('utf-8'))

    return render(request, 'resource_tracking/graph/resource-tracker-graph.html', context={'svg': svg})


def create_resource_pool_svg(resource_pool: ResourcePool):
    context = dict()
    context['name'] = {
        'display': resource_pool.name,
        'tooltip': f"Go to {resource_pool}",
        'href': reverse('resource_tracker:resource_pool_edit',
                        kwargs={'resource_pool_id': resource_pool.id})}

    context['attributes_list'] = [
        {
            'name': {
                'display': attribute.name,
                'tooltip': f"Go to {attribute}",
                'href': reverse('resource_tracker:resource_pool_attribute_edit',
                                kwargs={'resource_pool_id': resource_pool.id,
                                        'attribute_id': attribute.id})},
            'produced': {
                'display': attribute.get_total_produced(),
                'tooltip': f"Go to {attribute}'s producers",
                'href': reverse(
                    'resource_tracker:resource_pool_attribute_producer_list',
                    kwargs={'resource_pool_id': resource_pool.id,
                            'attribute_id': attribute.id})},
            'consumed': {
                'display': f"{attribute.get_total_consumed()} ({attribute.get_percent_consumed()}%)",
                'tooltip': f"Go to {attribute}'s consumers",
                'href': reverse(
                    'resource_tracker:resource_pool_attribute_consumer_list',
                    kwargs={'resource_pool_id': resource_pool.id,
                            'attribute_id': attribute.id})},
            'available': {
                'display': f"{attribute.get_total_produced() - attribute.get_total_consumed()} ({100 - attribute.get_percent_consumed()}%)",
                'color': get_progress_bar_color(attribute.get_percent_consumed())},
        }
        for attribute in resource_pool.attributes_definition.filter()]
    context['color'] = COLORS['resource_pool']
    context['color_available'] = COLORS['available']

    tm = get_template('resource_tracking/graph/resource_pool.j2').template
    return tm.render(context=Context(context))


def create_resource_group_svg(resource_group: ResourceGroup):
    context = dict()
    context['name'] = {
        'display': resource_group.name,
        'tooltip': f"Go to {resource_group}",
        'href': reverse('resource_tracker:resource_group_edit',
                        kwargs={'resource_group_id': resource_group.id})}
    context['count'] = {
        'display': resource_group.resources.count(),
        'tooltip': f"Go to {resource_group}'s resources",
        'href': reverse('resource_tracker:resource_group_resource_list',
                        kwargs={'resource_group_id': resource_group.id})}
    context['attributes_list'] = [
        {
            'key': attribute.name,
            'value': attribute.get_total_resource(),
            'tooltip': f"Go to {attribute}",
            'href': reverse('resource_tracker:resource_group_attribute_edit',
                            kwargs={'resource_group_id': resource_group.id,
                                    'attribute_id': attribute.id})
        }
        for attribute in resource_group.attribute_definitions.filter()
    ]
    context['color'] = COLORS['resource_group']

    tm = get_template('resource_tracking/graph/resource_group.j2').template
    return tm.render(context=Context(context))


def get_progress_bar_color(progress_value):
    if progress_value < 80:
        return COLORS["bg-green"]
    if 80 < progress_value < 90:
        return COLORS["bg-yellow"]
    return COLORS["bg-red"]