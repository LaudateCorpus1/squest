from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from resource_tracker.api.serializers.resource_group.resource_serializers import ResourceSerializer, \
    ResourceCreateSerializer
from resource_tracker.models import Resource, ResourceGroup


class ResourceListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ResourceSerializer

    def get_queryset(self):
        resource_group_id = self.kwargs['resource_group_id']
        queryset = Resource.objects.filter(resource_group_id=resource_group_id)
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset

    def create(self, request, **kwargs):
        resource_group_id = self.kwargs['resource_group_id']
        try:
            resource_group = get_object_or_404(ResourceGroup, pk=resource_group_id)
            context = {'resource_group': resource_group}
            serializer = ResourceCreateSerializer(data=request.data, context=context)
            if serializer.is_valid():
                new_resource = serializer.save()
                read_serializer = ResourceSerializer(instance=new_resource)
                return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise NotFound()


class ResourceGetDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ResourceSerializer

    def get_object(self):
        resource_group_id = self.kwargs.get('resource_group_id')
        resource_id = self.kwargs.get('resource_id')
        resource = get_object_or_404(Resource, id=resource_id,
                                     resource_group_id=resource_group_id)
        return resource
