# -*- coding: utf-8 -*-

"""Views module."""
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from suit_dashboard import Box, Column, DashboardView, Grid, Row

from .apps import AppSettings
from .models import RolePrivilege, get_role_id, get_role_type

app_settings = AppSettings()


class Index(DashboardView):
    """Cerberus menu."""

    title = _('Index - Cerberus AC')
    crumbs = (
        {'name': _('Home'), 'url': 'admin:index'},
        {'name': _('Cerberus AC'), 'url': 'admin:cerberus:index'},
    )
    grid = Grid(Row(Column(Box(
        title='Cerberus Access Control',
        template='cerberus_ac/index.html'))))


class MemberList(Index):
    """View to see the list of members."""

    title = _('Member List - Cerberus AC')
    crumbs = ({'name': _('Member List'), 'url': 'admin:cerberus:member_list'},)

    def get(self, request, *args, **kwargs):
        role_instances = []
        for r in app_settings.mapping.role_classes():
            role_instances.extend(r.objects.all())

        paginator = Paginator(role_instances, 50)

        page = request.GET.get('page_user_list')
        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            user_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            user_list = paginator.page(paginator.num_pages)

        self.grid = Grid(Row(Column(Box(template='cerberus_ac/member_info.html',
                               context={'members': user_list}))))


class MemberInfo(MemberList):
    """View to see member info."""

    title = _('Member Info - Cerberus AC')
    crumbs = ({'name': _('Member Info'), 'url': 'admin:cerberus:member_info'},)

    def get(self, request, *args, **kwargs):
        member_id = kwargs.pop('member_id')
        member_type = kwargs.pop('member_type')

        member = app_settings.mapping.instance_from_name_and_id(
            member_type, int(member_id))

        self.grid = Grid(Row(Column(Box(
            template='cerberus_ac/member_info.html',
            context={'member': member}))))

        return super(MemberInfo, self).get(request, *args, **kwargs)


class Logs(Index):
    """Cerberus Logs Menu."""

    title = _('Logs - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus:cerberus_logs'},)
    grid = Grid(Row(Column(Box(
        title='Logs',
        template='cerberus_ac/logs.html'))))


class Privileges(Index):
    """Menu for privileges."""

    context = {'role_types': [{
        'verbose': app_settings.mapping.class_from_name(t)._meta.verbose_name,
        'slug': t} for t in app_settings.mapping.role_types()
    ], 'resource_types': [{
        'verbose': app_settings.mapping.class_from_name(t)._meta.verbose_name,
        'slug': t} for t in app_settings.mapping.resource_types()
    ]}

    title = _('Privileges - Cerberus AC')
    crumbs = ({'name': _('Privileges'), 'url': 'admin:cerberus:privileges'},)
    grid = Grid(Row(Column(Box(template='cerberus_ac/privileges.html',
                               context=context))))


class ViewPrivileges(Privileges):
    """View to see user privileges."""

    title = _('View Privileges - Cerberus AC')
    crumbs = ({'name': _('View'), 'url': 'admin:cerberus:view_privileges'}, )

    def get(self, request, *args, **kwargs):
        role_type = kwargs.pop('role_type')
        resource_type = kwargs.pop('resource_type')
        role_class = app_settings.mapping.class_from_name(role_type)
        resource_class = app_settings.mapping.class_from_name(resource_type)
        role_instances = role_class.objects.all()
        resource_instances = resource_class.objects.all()
        self.grid = Grid(Row(Column(Box(
            template='cerberus_ac/view_privileges.html',
            context={'roles': role_instances, 'resources': resource_instances}
        ))))

        return super(ViewPrivileges, self).get(request, *args, **kwargs)


class EditPrivileges(Privileges):
    """View to edit user privileges."""

    title = _('Edit Privileges - Cerberus AC')
    crumbs = ({'name': _('Edit')}, )

    def get_paginated_data(self, instances, page):
        paginator = Paginator(instances, 50)

        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            paginated_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            paginated_data = paginator.page(paginator.num_pages)

        return paginated_data

    def get(self, request, *args, **kwargs):
        role_type = kwargs.pop('role_type')
        resource_type = kwargs.pop('resource_type')
        role_class = app_settings.mapping.class_from_name(role_type)
        resource_class = app_settings.mapping.class_from_name(resource_type)
        role_instances = role_class.objects.all()
        resource_instances = resource_class.objects.all()

        # role_instances = self.get_paginated_data(
        #     role_instances, request.GET.get('page_role'))
        # resource_instances = self.get_paginated_data(
        #     resource_instances, request.GET.get('page_resource'))

        self.grid = Grid(Row(Column(
            Box(template='cerberus_ac/edit_privileges_no_datatable.html',
                context={'roles': role_instances,
                         'resources': resource_instances,
                         'role_type': role_type,
                         'resource_type': resource_type})
        )))

        return super(EditPrivileges, self).get(request, *args, **kwargs)


def json_info(request, role_type, resource_type):
    role_class = app_settings.mapping.class_from_name(role_type)
    resource_class = app_settings.mapping.class_from_name(resource_type)
    role_instances = role_class.objects.all()
    resource_instances = resource_class.objects.all()

    res_list_json = json.dumps(
        [{'name': str(res)} for res in resource_instances])

    return HttpResponse(res_list_json, content_type="application/json")


def edit_perm_post(request, user):
    """Handler for user privileges POSTs."""
    if request.method == "POST":
        form = UserPermForm(request.POST)


class AccessHistory(Logs):
    """Cerberus Object Access Logs."""

    title = _('Object Access - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus:access_history'},)
    grid = Grid(Row(Column(Box(
        title='Object Access',
        template='cerberus_ac/access_history.html'))))


class PrivilegeHistory(Logs):
    """Cerberus Permission changes Logs."""

    title = _('Permission Changes - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus:privilege_history'},)  # noqa
    grid = Grid(Row(Column(Box(
        title='Permission Changes',
        template='cerberus_ac/privilege_history.html'))))


def edit_privileges_ajax(request,
                         role_type,
                         resource_type,
                         role_id,
                         resource_id,
                         privilege,
                         action):
    user = request.user
    success = False

    if not user.can('update', 'role_privilege'):
        message = _("You don't have the authorization to edit privileges")

    elif get_role_type(user) == role_type and get_role_id(user) == role_id:
        message = _("You can't edit your own privileges")

    elif action in ('allow', 'deny'):
        func = getattr(RolePrivilege, action)
        privilege, created = func(role_type, role_id, privilege,
                                  resource_type, resource_id, user)
        success = True
        if created:
            message = _('Successfully created privilege')
        else:
            message = _('Successfully updated privilege')
    elif action == 'forget':
        deleted = RolePrivilege.forget(role_type, role_id, privilege,
                                       resource_type, resource_id, user)
        if deleted:
            success = True
            message = _('Successfully deleted privilege')
        else:
            message = _('Privilege did not exist')
    else:
        message = _('Invalid request: action parameter accepts '
                    'allow, deny or forget')

    return HttpResponse(json.dumps({'success': success, 'message': message}),
                        content_type='application/json')
