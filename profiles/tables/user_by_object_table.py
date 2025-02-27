from django.contrib.auth.models import User
from django_tables2 import tables, TemplateColumn


class UserByObjectTable(tables.Table):
    actions = TemplateColumn(template_name='custom_columns/user_by_group_actions.html', orderable=False)
    role = TemplateColumn(template_name='custom_columns/role_object.html', orderable=False)

    class Meta:
        model = User
        attrs = {"id": "user_by_team_table", "class": "table squest-pagination-tables "}
        fields = ("username", "email", "role", "actions")
