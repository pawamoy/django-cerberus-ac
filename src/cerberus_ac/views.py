# -*- coding: utf-8 -*-

"""Views module."""
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from suit_dashboard import Box, Column, DashboardView, Grid, Row

from .apps import AppSettings
from .models import RoleHierarchy, RolePrivilege, get_role_id, get_role_type

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
            user_list = paginator.page(1)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages)

        self.grid = Grid(Row(Column(Box(
            title=_('Member list'),
            template='cerberus_ac/member_list.html',
            context={'members': user_list}))))

        return super(MemberList, self).get(request, *args, **kwargs)


class MemberInfo(Index):
    """View to see member info."""

    title = _('Member Info - Cerberus AC')
    crumbs = (
        {'name': _('Member List'), 'url': 'admin:cerberus:member_list'},
        {'name': _('Member Info')}
    )

    def get(self, request, *args, **kwargs):
        user_class = app_settings.mapping.user_classes()[0]
        user = user_class.objects.get(id=kwargs['member_id'])

        self.grid = Grid(Row(Column(Box(
            template='cerberus_ac/member_info.html',
            context={'member': user}))))

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

    title = _('Privileges Matrix - Cerberus AC')
    crumbs = ({'name': _('Privileges Matrix'),
               'url': 'admin:cerberus:privileges'},)
    grid = Grid(Row(Column(Box(
        title=_('Privileges Matrix'),
        template='cerberus_ac/privileges.html',
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


def get_paginated_data(instances, page, num):
    paginator = Paginator(instances, num)

    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        paginated_data = paginator.page(paginator.num_pages)
    return paginated_data


class EditPrivileges(Privileges):
    """View to edit user privileges."""

    title = _('Edit Privileges - Cerberus AC')
    crumbs = ({'name': _('Edit')}, )

    # def get_filtered_roles(self, queryset, string):
    #     return queryset
    #
    # def get_filtered_resources(self, queryset, string):
    #     return queryset

    def get(self, request, *args, **kwargs):
        role_type = kwargs.pop('role_type')
        resource_type = kwargs.pop('resource_type')
        role_class = app_settings.mapping.class_from_name(role_type)
        resource_class = app_settings.mapping.class_from_name(resource_type)
        role_instances = role_class.objects.all()
        resource_instances = resource_class.objects.all()

        # role_string = request.GET.get('role_string')
        # resource_string = request.GET.get('resource_string')
        # role_instances = self.get_filtered_roles(role_instances, role_string)
        # resource_instances = self.get_filtered_resources(
        #     resource_instances, resource_string)

        # role_page = request.GET.get('role_page')
        # resource_page = request.GET.get('resource_page')
        # role_instances = role_instances.order_by('id')
        # resource_instances = resource_instances.order_by('id')
        # role_instances = get_paginated_data(role_instances, role_page, 40)
        # resource_instances = get_paginated_data(
        #     resource_instances, resource_page, 10)

        self.grid = Grid(Row(Column(
            Box(title=_('Edit role privileges between %s and %s') % (
                    role_class._meta.verbose_name_plural,
                    resource_class._meta.verbose_name_plural),
                template='cerberus_ac/edit_privileges_no_datatable.html',
                context={'roles': role_instances,
                         'resources': resource_instances,
                         'role_type': role_type,
                         'resource_type': resource_type})
        )))

        return super(EditPrivileges, self).get(request, *args, **kwargs)


def json_info(request, role_type, resource_type):
    # role_class = app_settings.mapping.class_from_name(role_type)
    resource_class = app_settings.mapping.class_from_name(resource_type)
    # role_instances = role_class.objects.all()
    resource_instances = resource_class.objects.all()

    res_list_json = json.dumps(
        [{'name': str(res)} for res in resource_instances])

    return HttpResponse(res_list_json, content_type="application/json")


def edit_perm_post(request, user):
    """Handler for user privileges POSTs."""
    # if request.method == "POST":
    #     form = UserPermForm(request.POST)
    pass


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

    elif (not app_settings.allow_update_own_privileges and
          get_role_type(user) == role_type and
          get_role_id(user) == role_id):
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


def edit_privileges_json(request, role_type, resource_type):
    role_class = app_settings.mapping.class_from_name(role_type)
    resource_class = app_settings.mapping.class_from_name(resource_type)
    role_instances = role_class.objects.order_by('id')
    resource_instances = resource_class.objects.order_by('id')

    body = []
    head = []
    default_access_types = ('read', 'update', 'delete')

    for role in role_instances:
        row = [role.id, str(role)]
        for resource in resource_instances:
            str_res = str(resource)
            head.append(str_res)
            row.extend([resource.id, str_res])
            current_privileges = []
            db_access_types = []
            for privilege in RolePrivilege.objects.filter(
                    role_type=role_type, role_id=role.id,
                    resource_type=resource_type, resource_id=resource.id):
                current_privileges.append([privilege.access_type,
                                           privilege.authorized])
                db_access_types.append(privilege.access_type)
            for default_access_type in default_access_types:
                if default_access_type not in db_access_types:
                    current_privileges.append([default_access_type, False])
            row.append(current_privileges)
        body.append(row)

    data = {
        'head': head,
        'body': body
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


class ViewRoleHierarchy(Index):
    """Role hierarchy view."""

    title = _('Role Hierarchy Graph - Cerberus AC')
    crumbs = ({'name': _('Role Hierarchy Graph'),
               'url': 'admin:cerberus:role_hierarchy'},)

    def get(self, request, *args, **kwargs):
        data = [{'source': '%s %s' % (rh.role_type_b, rh.role_id_b),
                 'target': '%s %s' % (rh.role_type_a, rh.role_id_a),
                 'type': 'suit'}
                for rh in RoleHierarchy.objects.all()]

        self.grid = Grid(Row(Column(Box(
            title='Role Hierarchy Graph',
            template='cerberus_ac/view_role_hierarchy.html',
            context=json.dumps(data)))))

        return super(ViewRoleHierarchy, self).get(request, *args, **kwargs)
