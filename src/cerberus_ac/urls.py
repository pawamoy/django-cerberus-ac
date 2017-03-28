from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^permissions/group/edit/$', views.edit_group_perm_post, name='edit_group_permissions_post'),
    url(r'^permissions/group/edit/$', views.edit_group_perm, name='edit_group_permissions'),
    url(r'^permissions/group/view/$', views.view_group_perm, name='view_group_permissions'),
    url(r'^permissions/user/view/(?P<user>[0-9]+)/$', views.edit_user_perm_post, name='edit_user_permissions_post'),
    url(r'^permissions/user/view/(?P<user>[0-9]+)/$', views.edit_user_perm, name='edit_user_permissions'),
    url(r'^permissions/user/view/$', views.view_user_perm, name='view_user_permissions'),
    url(r'^member_info/$', views.member_info, name='view_member_info'),
    url(r'^logs/object_access/$', views.logs_access, name='logs_access'),
    url(r'^logs/permission_changes/$', views.perm_changes, name='perm_changes'),
    url(r'^permissions/role/hierarchy/$', views.role_hierarchy, name='role_hierarchy'),
]