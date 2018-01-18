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

        # role views
        url(r'^privileges/view/(?P<role_type>\w+)/(?P<resource_type>\w+)/$',
            admin_view_func(views.ViewPrivileges.as_view()),
            name='view_privileges'),
        url(r'^privileges/edit/(?P<role_type>\w+)/(?P<resource_type>\w+)/$',
            admin_view_func(views.EditPrivileges.as_view()),
            name='edit_privileges'),
        url(r'^privileges/edit/(?P<role_type>\w+)/(?P<resource_type>\w+)/'
            r'(?P<role_id>\w+)/(?P<resource_id>\w+)/(?P<privilege>\w+)/'
            r'(?P<action>\w+)/$',
            admin_view_func(views.ajax_edit_privileges),
            name='ajax_edit_privileges'),
        url(r'^privileges/load_rr/(?P<role_type>\w+)/(?P<resource_type>\w+)/',
            admin_view_func(views.ajax_load_roles_and_resources),
            name='ajax_load_roles_and_resources'),
        url(r'^privileges/load/(?P<role_type>\w+)/(?P<role_id>\w+)/'
            r'(?P<resource_type>\w+)/',
            admin_view_func(views.ajax_load_privileges),
            name='ajax_load_privileges'),

        # Member Info
        url(r'^members/$',
            admin_view_func(views.MemberList.as_view()),
            name='member_list'),
        url(r'^members/(?P<member_id>\d+)/$',
            admin_view_func(views.MemberInfo.as_view()),
            name='member_info'),

        # hierarchy
        url(r'^role/hierarchy/$',
            admin_view_func(views.ViewRoleHierarchy.as_view()),
            name='role_hierarchy')
    ]


app_name = AppSettings.namespace.get_value()
urlpatterns = cerberus_urlpatterns()
