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

        url(r'^privileges/$',
            admin_view_func(views.Privileges.as_view()),
            name='privileges'),

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
        url(r'^privileges/edit/json/$',
            admin_view_func(views.json_info),
            name='edit_user_privileges_json'),
        url(r'^privileges/edit/(?P<user>\d+)/$',
            admin_view_func(views.edit_user_perm_post),
            name='edit_user_privileges_post'),

        # other views
        url(r'^member_info/(?P<member_type>\w+)/(?P<member_id>\d+)/$',
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
