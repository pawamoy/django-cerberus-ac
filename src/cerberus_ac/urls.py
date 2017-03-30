# -*- coding: utf-8 -*-

"""URLs module."""

from django.conf.urls import url

from . import views


def cerberus_urlpatterns(admin_view):
    return [
        # url(r'^$', admin_view(views.index), name='index'),

        # user views
        # url(r'^permissions/user/view/$',
        #     admin_view(views.ViewUserPerm.as_view()),
        #     name='view_user_permissions'),
        url(r'^permissions/user/edit/$',
            admin_view(views.EditUserPerm.as_view()),
            name='edit_user_permissions'),
        url(r'^permissions/user/edit/(?P<user>[0-9]+)/$',
            admin_view(views.edit_user_perm_post),
            name='edit_user_permissions_post'),

        # group views
        # url(r'^permissions/group/view/$',
        #     admin_view(views.ViewGroupPerm.as_view()),
        #     name='view_group_permissions'),
        url(r'^permissions/group/edit/$',
            admin_view(views.EditGroupPerm.as_view()),
            name='edit_group_permissions'),
        url(r'^permissions/group/edit/(?P<group>[0-9]+)/$',
            admin_view(views.edit_group_perm_post),
            name='edit_group_permissions_post'),

        # other views
        # url(r'^member_info/$',
        #     admin_view(views.MemberInfo.as_view()),
        #     name='view_member_info'),
        # url(r'^logs/object_access/$',
        #     admin_view(views.ObjectAccess.as_view()),
        #     name='logs_access'),
        # url(r'^logs/permission_changes/$',
        #     admin_view(views.PermChanges.as_view()),
        #     name='perm_changes'),
    ]
