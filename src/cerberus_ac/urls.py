# -*- coding: utf-8 -*-

"""URLs module."""

from django.conf.urls import url

from . import views


def cerberus_urlpatterns(admin_view_func=lambda x: x):
    """
    Function returning URLs, optionally wrapped into an admin_view function.

    Args:
        admin_view_func (func):
            the ``admin_view`` function of an ``AdminSite``. Will default to
            identity.

    Returns:
        list: list of URLs patterns.
    """
    return [
        url(r'^$', admin_view_func(views.Index.as_view()),
            name='cerberus_index'),

        url(r'^permissions/$',
            admin_view_func(views.Permissions.as_view()),
            name='permissions'),

        url(r'logs/$',
            admin_view_func(views.Logs.as_view()),
            name='logs'),

        # role views
        url(r'^privileges/view/(?P<role_type>\w+)/(?P<resource_type>\w+)/$',
            admin_view_func(views.ViewPrivileges.as_view()),
            name='view_privileges'),
        url(r'^privileges/edit/(?P<role_type>\w+)/(?P<resource_type>\w+)/$',
            admin_view_func(views.EditPrivileges.as_view()),
            name='edit_privileges'),

        # user views
        url(r'^permissions/user/$',
            admin_view_func(views.UserPermissions.as_view()),
            name='user_permissions'),
        url(r'^permissions/user/view/$',
            admin_view_func(views.ViewUserPermissions.as_view()),
            name='view_user_permissions'),
        url(r'^permissions/user/edit/$',
            admin_view_func(views.EditUserPermissions.as_view()),
            name='edit_user_permissions'),
        url(r'^permissions/user/edit/(?P<user>\d+)/$',
            admin_view_func(views.edit_user_perm_post),
            name='edit_user_permissions_post'),

        # group views
        url(r'^permissions/group/$',
            admin_view_func(views.GroupPermissions.as_view()),
            name='group_permissions'),
        url(r'^permissions/group/view/$',
            admin_view_func(views.ViewGroupPermissions.as_view()),
            name='view_group_permissions'),
        url(r'^permissions/group/edit/$',
            admin_view_func(views.EditGroupPermissions.as_view()),
            name='edit_group_permissions'),
        url(r'^permissions/group/edit/(?P<group>\d+)/$',
            admin_view_func(views.edit_group_perm_post),
            name='edit_group_permissions_post'),

        # other views
        url(r'^member_info/$',
            admin_view_func(views.MemberInfo.as_view()),
            name='view_member_info'),
        url(r'^logs/object_access/$',
            admin_view_func(views.ObjectAccess.as_view()),
            name='logs_access'),
        url(r'^logs/permission_changes/$',
            admin_view_func(views.PermChanges.as_view()),
            name='perm_changes'),

    ]


urlpatterns = cerberus_urlpatterns()
