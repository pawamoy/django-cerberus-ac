# -*- coding: utf-8 -*-

"""URLs module."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index,
        name='index'),
    url(r'^permissions/group/edit/$', views.editgrouppermpost,
        name='edit_group_permissions_post'),
    url(r'^permissions/group/edit/$', views.editgroupperm,
        name='edit_group_permissions'),
    url(r'^permissions/group/view/$', views.viewgroupperm,
        name='view_group_permissions'),
    url(r'^permissions/user/view/(?P<user>[0-9]+)/$', views.edituserpermpost,
        name='edit_user_permissions_post'),
    url(r'^permissions/user/view/(?P<user>[0-9]+)/$', views.edituserperm,
        name='edit_user_permissions'),
    url(r'^permissions/user/view/$', views.viewuserperm,
        name='view_user_permissions'),
    url(r'^member_info/$', views.memberinfo,
        name='view_member_info'),
    url(r'^logs/object_access/$', views.logs_access,
        name='logs_access'),
    url(r'^logs/permission_changes/$', views.perm_changes,
        name='perm_changes'),
]
