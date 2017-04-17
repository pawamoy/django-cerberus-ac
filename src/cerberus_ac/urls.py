# -*- coding: utf-8 -*-

"""URLs module."""

from django.conf.urls import url

from . import views
from .apps import AppSettings


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
            name='index'),

        url(r'^privileges/$',
            admin_view_func(views.Privileges.as_view()),
            name='privileges'),

        url(r'logs/$',
            admin_view_func(views.Logs.as_view()),
            name='logs'),

        url(r'member/$',
            admin_view_func(views.MemberList.as_view()),
            name='member'),

        # role views
        url(r'^privileges/view/(?P<role_type>\w+)/(?P<resource_type>\w+)/$',
            admin_view_func(views.ViewPrivileges.as_view()),
            name='view_privileges'),
        url(r'^privileges/edit/(?P<role_type>\w+)/(?P<resource_type>\w+)/$',
            admin_view_func(views.EditPrivileges.as_view()),
            name='edit_privileges'),
        url(r'^privileges/edit/(?P<role_type>\w+)/(?P<resource_type>\w+)/'
            r'json/$',
            admin_view_func(views.json_info),
            name='edit_privileges_json'),
        url(r'^privileges/edit/(?P<role_type>\w+)/(?P<resource_type>\w+)/'
            r'(?P<role_id>\w+)/(?P<resource_id>\w+)/(?P<privilege>\w+)/'
            r'(?P<action>\w+)/$',
            admin_view_func(views.edit_privileges_ajax),
            name='edit_privileges_ajax'),
        url(r'^privileges/edit/(?P<user>\d+)/$',
            admin_view_func(views.edit_perm_post),
            name='edit_privileges_post'),

        # Member Info
        url(r'^members/$',
            admin_view_func(views.MemberList.as_view()),
            name='member_list'),
        url(r'^members/(?P<member_id>\d+)/$',
            admin_view_func(views.MemberInfo.as_view()),
            name='member_info'),

        # history views
        url(r'^history/access/$',
            admin_view_func(views.AccessHistory.as_view()),
            name='access_history'),
        url(r'^history/privileges/$',
            admin_view_func(views.PrivilegeHistory.as_view()),
            name='privilege_history'),

        # hierarchy
        url(r'^role/hierarchy/$',
            admin_view_func(views.ViewRoleHierarchy.as_view()),
            name='role_hierarchy')
    ]


app_name = AppSettings.get_namespace()
urlpatterns = cerberus_urlpatterns()
