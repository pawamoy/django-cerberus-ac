# -*- coding: utf-8 -*-

"""Views module."""

from django.utils.translation import ugettext as _

from suit_dashboard import Box, Column, DashboardView, Grid, Row

from . import AppSettings

resources_list = AppSettings.get_actual_resources_classes()
role_classes = AppSettings.get_actual_roles_classes()


def edit_user_perm_post(request, user):
    """Handler for user permissions POSTs."""
    if request.method == "POST":
        pass


class EditUserPerm(DashboardView):
    """Dashboard view to see user permissions."""
    title = _('Edit User Permissions')
    crumbs = (
        {'name': _('Cerberus')},
        {'name': _('Permissions')},
        {'name': _('Users')},
        {'name': _('Edit'), 'url': 'admin:edit_user_perm'}
    )

    role_instances = []
    for r in role_classes:
        role_instances.extend(r.objects.all())

    resources_real_list = []
    for res in resources_list:
        resources_real_list.extend(res.objects.all())

    grid = Grid(Row(Column(
        Box(template='cerberus_ac/edit_user_perms.html',
            context={'members': role_instances[:10:],
                     'resources': resources_real_list[:10:]})
    )))


def edit_group_perm_post(request, user):
    """Handler for group permissions POSTs."""
    if request.method == "POST":
        pass


class EditGroupPerm(DashboardView):
    """Dashboard view to see group permissions."""

    role_instances = []
    for r in role_classes:
        role_instances.extend(r.objects.all())

    resources_real_list = []
    for res in resources_list:
        resources_real_list.extend(res.objects.all())

    grid = Grid(Row(Column(
        Box(template='cerberus_ac/edit_user_perms.html',
            context={'members': role_instances,
                     'resources': resources_real_list})
    )))
