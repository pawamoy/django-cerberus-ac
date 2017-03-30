# -*- coding: utf-8 -*-

"""Views module."""

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
