# -*- coding: utf-8 -*-

"""Views module."""

from django.utils.translation import ugettext as _

from suit_dashboard import Box, Column, DashboardView, Grid, Row

from . import AppSettings


app_settings = AppSettings()


class Index(DashboardView):
    """Cerberus menu."""

    title = _('Index - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus_index'}, )
    grid = Grid(Row(Column(Box(
        title='Cerberus Access Control',
        template='cerberus_ac/index.html'))))


class MemberInfo(Index):
    """View to see member info."""

    title = _('Member Info - Cerberus AC')
    crumbs = ({'name': _('Member Info'), 'url': 'admin:member_info'}, )
    grid = Grid(Row(Column(Box(template='cerberus_ac/member_info.html'))))


class Logs(Index):
    """Cerberus Logs Menu."""

    title = _('Logs - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus_logs'},)
    grid = Grid(Row(Column(Box(
        title='Logs',
        template='cerberus_ac/logs.html'))))


class Permissions(Index):
    """Menu for permissions."""

    title = _('Permissions - Cerberus AC')
    crumbs = ({'name': _('Permissions'), 'url': 'admin:permissions'}, )
    grid = Grid(Row(Column(Box(template='cerberus_ac/permissions.html'))))


class UserPermissions(Permissions):
    """Menu for user permissions."""

    title = _('User Permissions - Cerberus AC')
    crumbs = ({'name': _('User'), 'url': 'admin:user_permissions'}, )
    grid = Grid(Row(Column(Box(template='cerberus_ac/user_permissions.html'))))


class ViewUserPermissions(UserPermissions):
    """View to see user permissions."""

    title = _('View User Permissions - Cerberus AC')
    crumbs = ({'name': _('View'), 'url': 'admin:view_user_permissions'}, )
    grid = Grid(Row(Column(Box(template='cerberus_ac/view_user_permissions.html'))))  # noqa


class EditUserPermissions(UserPermissions):
    """View to edit user permissions."""

    title = _('Edit User Permissions - Cerberus AC')
    crumbs = ({'name': _('Edit'), 'url': 'admin:edit_user_permissions'}, )

    role_instances = []
    for r in app_settings.mapping.role_classes():
        role_instances.extend(r.objects.all())

    resources_real_list = []
    for res in app_settings.mapping.resource_classes():
        resources_real_list.extend(res.objects.all())

    grid = Grid(Row(Column(
        Box(template='cerberus_ac/edit_user_permissions.html',
            context={'members': role_instances[:10:],
                     'resources': resources_real_list[:10:]})
    )))


def edit_user_perm_post(request, user):
    """Handler for user permissions POSTs."""
    if request.method == "POST":
        pass


class GroupPermissions(Permissions):
    """Menu for group permissions."""

    title = _('Group Permissions - Cerberus AC')
    crumbs = ({'name': _('Group'), 'url': 'admin:group_permissions'}, )
    grid = Grid(Row(Column(Box(template='cerberus_ac/group_permissions.html'))))  # noqa


class ViewGroupPermissions(GroupPermissions):
    """View to see user permissions."""

    title = _('View Group Permissions - Cerberus AC')
    crumbs = ({'name': _('View'), 'url': 'admin:view_group_permissions'}, )
    grid = Grid(Row(Column(Box(template='cerberus_ac/view_group_permissions.html'))))  # noqa


class EditGroupPermissions(GroupPermissions):
    """View to edit group permissions."""

    title = _('Edit Group Permissions - Cerberus AC')
    crumbs = ({'name': _('Edit'), 'url': 'admin:edit_group_permissions'}, )

    role_instances = []
    for r in app_settings.mapping.role_classes():
        role_instances.extend(r.objects.all())

    resources_real_list = []
    for res in app_settings.mapping.resource_classes():
        resources_real_list.extend(res.objects.all())

    grid = Grid(Row(Column(
        Box(template='cerberus_ac/edit_group_permissionss.html',
            context={'members': role_instances,
                     'resources': resources_real_list})
    )))


def edit_group_perm_post(request, user):
    """Handler for group permissions POSTs."""
    if request.method == "POST":
        pass


class ObjectAccess(Logs):
    """Cerberus Object Access Logs"""

    title = _('Object Access - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus_obj_acc_logs'},)
    grid = Grid(Row(Column(Box(
        title='Object Access',
        template='cerberus_ac/obj_access_logs.html'))))


class PermChanges(Logs):
    """Cerberus Permission changes Logs."""

    title = _('Permission Changes - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus_perm_changes_logs'},)
    grid = Grid(Row(Column(Box(
        title='Permission Changes',
        template='cerberus_ac/perms_changes_logs.html'))))


