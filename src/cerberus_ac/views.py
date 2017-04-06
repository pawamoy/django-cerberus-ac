# -*- coding: utf-8 -*-

"""Views module."""
from django.core import serializers
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from suit_dashboard import Box, Column, DashboardView, Grid, Row

from . import AppSettings

from .models import *

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

    context = {'role_types': [{
        'verbose': app_settings.mapping.class_from_name(t)._meta.verbose_name,
        'slug': t} for t in app_settings.mapping.role_types()
    ], 'resource_types': [{
        'verbose': app_settings.mapping.class_from_name(t)._meta.verbose_name,
        'slug': t} for t in app_settings.mapping.resource_types()
    ]}

    title = _('Permissions - Cerberus AC')
    crumbs = ({'name': _('Permissions'), 'url': 'admin:permissions'}, )
    grid = Grid(Row(Column(Box(template='cerberus_ac/permissions.html',
                               context=context))))


class ViewPrivileges(Permissions):
    """View to see user permissions."""

    title = _('View Privileges - Cerberus AC')

    def get(self, request, *args, **kwargs):
        self.crumbs = ({'name': _('View'), 'url': 'admin:view_privileges'}, )
        self.grid = Grid(Row(Column(Box(template='cerberus_ac/view_privileges.html'))))  # noqa
        return super(ViewPrivileges, self).get(request, *args, **kwargs)


class EditPrivileges(Permissions):
    """View to edit user permissions."""

    title = _('Edit Privileges - Cerberus AC')

    def get(self, request, *args, **kwargs):
        self.crumbs = ({'name': _('Edit'), 'url': 'admin:edit_privileges'}, )
        self.grid = Grid(Row(Column(Box(template='cerberus_ac/edit_privileges.html'))))  # noqa
        return super(EditPrivileges, self).get(request, *args, **kwargs)


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

    def get_user_list(self, request):
        role_instances = []
        for r in app_settings.mapping.role_classes():
            role_instances.extend(r.objects.all())

        # paginator = Paginator(role_instances, 50)
        #
        # page = request.GET.get('page_role')
        # try:
        #     user_list = paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer, deliver first page.
        #     user_list = paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range (e.g. 9999), deliver last page of results.
        #     user_list = paginator.page(paginator.num_pages)
        #
        # user_list_json = json.dumps(user_list)

        return role_instances

    def get_user_list_json(self, request):
        role_instances = []
        for r in app_settings.mapping.role_classes():
            role_instances.extend(r.objects.all().values('id', 'username'))

        user_list_json = serializers.serialize('json', r.objects.all(), fields=('id', 'username'))

        # user_list_json = json.dumps([{'id': role.id, 'name': role.username} for role in role_instances])

        return HttpResponse(user_list_json, content_type='application/json')

    def get_res_list(self, request):
        resources_real_list = []
        for res in app_settings.mapping.resource_classes():
            resources_real_list.extend(res.objects.all())

        return resources_real_list

    def get_res_list_json(self, request):
        resources_real_list = []
        for res in app_settings.mapping.resource_classes():
            resources_real_list.extend(res.objects.all().values('id', ''))

        res_list_json = serializers.serialize('json', res.objects.all(), fields=('id', ''))

        # json.dumps([{'id': res.id, 'name': res} for res in resources_real_list])

        return HttpResponse(res_list_json, content_type='application/json')

    def get(self, request, *args, **kwargs):
        self.grid = Grid(Row(Column(
            Box(template='cerberus_ac/edit_user_permissions.html',
                context={'members': self.get_user_list(request),
                         'resources': self.get_res_list_json(request),
                         'members_json': self.get_user_list_json(request),
                         'resources_json': self.get_res_list_json(request)})
        )))



        return super(EditUserPermissions, self).get(request, *args, **kwargs)


def edit_user_perm_post(request, user, ):
    """Handler for user permissions POSTs."""
    if request.method == "POST":
        form = UserPermForm(request.POST)


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

    def get(self, request, *args, **kwargs):
        role_instances = []
        for r in app_settings.mapping.role_classes():
            role_instances.extend(r.objects.all())

        resources_real_list = []
        for res in app_settings.mapping.resource_classes():
            resources_real_list.extend(res.objects.all())

        self.grid = Grid(Row(Column(
            Box(template='cerberus_ac/edit_group_permissionss.html',
                context={'members': role_instances,
                         'resources': resources_real_list})
        )))

        return super(EditGroupPermissions, self).get(request, *args, **kwargs)


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
