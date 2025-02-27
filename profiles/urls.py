from django.conf.urls.static import static
from django.urls import path

from Squest import settings
from . import views
from .views.group_list_view import GroupListView
from .views.team_list_view import TeamListView
from .views.user_by_group_list_view import UserByGroupListView
from .views.user_list_view import UserListView

app_name = 'profiles'

urlpatterns = [
    # common URLs
    path('profile/', views.profile, name='profile'),
    path('profile/token/create/', views.token_create, name='token_create'),
    path('profile/token/<int:token_id>/generate/', views.token_generate, name='token_generate'),
    path('profile/token/<int:token_id>/edit/', views.token_edit, name='token_edit'),
    path('profile/token/<int:token_id>/delete/', views.token_delete, name='token_delete'),

    path('user/', UserListView.as_view(), name='user_list'),

    # group URLs
    path('group/<int:group_id>/users/', UserByGroupListView.as_view(), name='user_by_group_list'),
    path('group/<int:group_id>/users/update/', views.user_in_group_update, name='user_in_group_update'),
    path('group/<int:group_id>/users/remove/<int:user_id>/', views.user_in_group_remove, name='user_in_group_remove'),
    path('group/', GroupListView.as_view(), name='group_list'),
    path('group/create/', views.group_create, name='group_create'),
    path('group/<int:group_id>/edit/', views.group_edit, name='group_edit'),
    path('group/<int:group_id>/delete/', views.group_delete, name='group_delete'),

    # billing group URLs
    path('billing-group/<int:billing_group_id>/users/update/', views.user_in_billing_group_update,
         name='user_in_billing_group_update'),
    path('billing-group/<int:billing_group_id>/users/remove/<int:user_id>/',
         views.user_in_billing_group_remove, name='user_in_billing_group_remove'),
    path('billing-group/', views.billing_group_list, name='billing_group_list'),
    path('billing-group/create/', views.billing_group_create, name='billing_group_create'),
    path('billing-group/<int:billing_group_id>/edit/', views.billing_group_edit, name='billing_group_edit'),
    path('billing-group/<int:billing_group_id>/delete/', views.billing_group_delete, name='billing_group_delete'),
    path('billing-group/<int:billing_group_id>/refresh_quota/', views.billing_group_refresh_quota, name='billing_group_refresh_quota'),

    # Quota Binding
    path('billing-group/<int:billing_group_id>/quota_attribute/<int:quota_binding_id>/edit/', views.quota_binding_edit,
         name='quota_binding_edit'),
    path('billing-group/<int:billing_group_id>/quota_attribute/<int:quota_binding_id>/delete/',
         views.quota_binding_delete, name='quota_binding_delete'),
    path('billing-group/<int:billing_group_id>/quota_attribute/edit/', views.quota_binding_edit_all,
         name='quota_binding_edit_all'),
    path('billing-group/<int:billing_group_id>/quota_attribute/edit-limits/', views.quota_binding_set_limits,
         name='quota_binding_set_limits'),

    # notifications
    path('notification/switch/', views.notification_switch, name='notification_switch'),
    path('notification/add_service/', views.notification_add_service, name='notification_add_service'),
    path('notification/remove_service/<int:service_id>/', views.notification_remove_service,
         name='notification_remove_service'),

    # team URLs
    path('team/<int:team_id>/users/update/', views.user_in_team_update, name='user_in_team_update'),
    path('team/<int:team_id>/users/remove/<int:user_id>/', views.user_in_team_remove, name='user_in_team_remove'),
    path('team/', TeamListView.as_view(), name='team_list'),
    path('team/create/', views.team_create, name='team_create'),
    path('team/<int:team_id>/', views.team_details, name='team_details'),
    path('team/<int:team_id>/edit/', views.team_edit, name='team_edit'),
    path('team/<int:team_id>/delete/', views.team_delete, name='team_delete'),
    path('team/<int:team_id>/details/create-role/', views.create_team_binding, name='create_team_role_binding'),

    # User Role Binding URLs
    path('role/ajax/get-users-with-role/', views.ajax_get_users_with_role, name='get_users_with_role'),
    path('role/ajax/get-teams-with-role/', views.ajax_get_teams_with_role, name='get_teams_with_role'),

    path('role/ajax/update-roles/', views.ajax_team_role_binding_form_update_roles, name='ajax_update_roles'),
    path('role/ajax/update-objects/', views.ajax_team_role_binding_form_update_objects, name='ajax_update_objects'),

    # Quota
    path('quota/', views.QuotaListView.as_view(), name='quota_list'),
    path('quota/create/', views.quota_create, name='quota_create'),
    path('quota/<int:quota_id>/edit/', views.quota_edit,
         name='quota_edit'),
    path('quota/<int:quota_id>/delete/', views.quota_delete,
         name='quota_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
