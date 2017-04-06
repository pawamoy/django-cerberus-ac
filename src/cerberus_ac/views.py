# -*- coding: utf-8 -*-

"""Views module."""
import json

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from suit_dashboard import Box, Column, DashboardView, Grid, Row

from . import AppSettings


app_settings = AppSettings()


class Index(DashboardView):
    """Cerberus menu."""

    title = _('Index - Cerberus AC')
    crumbs = (
        {'name': _('Home'), 'url': 'admin:index'},
        {'name': _('Cerberus'), 'url': 'admin:cerberus_index'},
    )
    grid = Grid(Row(Column(Box(
        title='Cerberus Access Control',
        template='cerberus_ac/index.html'))))


class MemberInfo(Index):
    """View to see member info."""

    title = _('Member Info - Cerberus AC')
    crumbs = ({'name': _('Member Info'), 'url': 'admin:member_info'},)

    def get(self, request, *args, **kwargs):
        member_id = kwargs.pop('member_id'),
        member_type = kwargs.pop('member_type')

        member = app_settings.mapping.instance_from_name_and_id(member_type, int(member_id))

        self.grid = Grid(Row(Column(Box(
            template='cerberus_ac/member_info.html',
            context={'member': member}))))

        return super(MemberInfo, self).get(request, *args, **kwargs)


class MemberInfoList(Index):
    """View to see the list of members."""

    title = _('Member Info - Cerberus AC')
    crumbs = ({'name': _('Member Info'), 'url': 'admin:member_info'},)

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


class Logs(Index):
    """Cerberus Logs Menu."""

    title = _('Logs - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus_logs'},)
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
    crumbs = ({'name': _('Privileges'), 'url': 'admin:privileges'},)
    grid = Grid(Row(Column(Box(template='cerberus_ac/privileges.html',
                               context=context))))


class ViewPrivileges(Privileges):
    """View to see user privileges."""

    title = _('View Privileges - Cerberus AC')
    crumbs = ({'name': _('View'), 'url': 'admin:view_privileges'}, )

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
    crumbs = ({'name': _('Edit'), 'url': 'admin:edit_privileges'}, )

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
        #     # If page is out of range (e.g. 9999), deliver last page of results.  # noqa
        #     user_list = paginator.page(paginator.num_pages)
        #
        # user_list_json = json.dumps(user_list)

        return role_instances

    def get_res_list(self, request):
        resources_real_list = []
        for res in app_settings.mapping.resource_classes():
            resources_real_list.extend(res.objects.all())

        return resources_real_list

    def get(self, request, *args, **kwargs):
        role_type = kwargs.pop('role_type')
        resource_type = kwargs.pop('resource_type')
        role_class = app_settings.mapping.class_from_name(role_type)
        resource_class = app_settings.mapping.class_from_name(resource_type)
        role_instances = role_class.objects.all()
        resource_instances = resource_class.objects.all()
        self.grid = Grid(Row(Column(
            Box(template='cerberus_ac/edit_user_privileges.html',
                context={'members': role_instances,
                         'resources': resource_instances})
        )))

        return super(EditPrivileges, self).get(request, *args, **kwargs)


def json_info(request):
    role_instances = []
    for r in app_settings.mapping.role_classes():
        role_instances.extend(r.objects.all())

    resources_real_list = []
    for res in app_settings.mapping.resource_classes():
        resources_real_list.extend(res.objects.all())

    res_list_json = json.dumps([{'name': str(res)} for res in resources_real_list])

    return HttpResponse(res_list_json, content_type="application/json")


def edit_user_perm_post(request, user, ):
    """Handler for user privileges POSTs."""
    if request.method == "POST":
        form = UserPermForm(request.POST)


class ObjectAccess(Logs):
    """Cerberus Object Access Logs."""

    title = _('Object Access - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus_obj_acc_logs'},)
    grid = Grid(Row(Column(Box(
        title='Object Access',
        template='cerberus_ac/obj_access_logs.html'))))


class PermChanges(Logs):
    """Cerberus Permission changes Logs."""

    title = _('Permission Changes - Cerberus AC')
    crumbs = ({'name': _('Cerberus'), 'url': 'admin:cerberus_perm_changes_logs'},)  # noqa
    grid = Grid(Row(Column(Box(
        title='Permission Changes',
        template='cerberus_ac/perms_changes_logs.html'))))
