# -*- coding: utf-8 -*-

"""Views module."""

import json

from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.defaults import bad_request

from suit_dashboard import Box, Column, DashboardView, Grid, Row

from .apps import AppSettings
from .models import RoleHierarchy, RolePrivilege
from .utils import get_role_id, get_role_type

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
        member_class = app_settings.mapping.user_classes()[0]
        members = member_class.objects.all()

        # members = get_paginated_data(
        #     members, request.GET.get('page_user_list'), 50)

        self.grid = Grid(Row(Column(Box(
            title=_('Member list'),
            template='cerberus_ac/member_list.html',
            context={'members': members}))))

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


class Privileges(Index):
    """Menu for privileges."""

    context = {'role_types': [{
        'verbose': app_settings.mapping.get_class(t)._meta.verbose_name,
        'slug': t} for t in app_settings.mapping.role_types()
    ], 'resource_types': [{
        'verbose': app_settings.mapping.get_class(t)._meta.verbose_name,
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
        role_class = app_settings.mapping.get_class(role_type)
        resource_class = app_settings.mapping.get_class(resource_type)
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

    def get(self, request, *args, **kwargs):
        role_type = kwargs.pop('role_type')
        resource_type = kwargs.pop('resource_type')
        role_class = app_settings.mapping.get_class(role_type)
        resource_class = app_settings.mapping.get_class(resource_type)
        role_instances = role_class.objects.all()
        resource_instances = resource_class.objects.all()

        self.grid = Grid(Row(Column(
            Box(title=_('Edit role privileges between %s and %s') % (
                    role_class._meta.verbose_name_plural,
                    resource_class._meta.verbose_name_plural),
                template='cerberus_ac/edit_privileges.html',
                context={'roles': role_instances,
                         'resources': resource_instances,
                         'role_type': role_type,
                         'resource_type': resource_type})
        )))

        return super(EditPrivileges, self).get(request, *args, **kwargs)


class ViewRoleHierarchy(Index):
    """Role hierarchy view."""

    title = _('Role Hierarchy Graph - Cerberus AC')
    crumbs = ({'name': _('Role Hierarchy Graph'),
               'url': 'admin:cerberus:role_hierarchy'},)

    def get(self, request, *args, **kwargs):
        # link
        # {"source": 3, "target": 11}
        # node
        # {"size": 10, "score": 0, "id": "security", "type": "circle"}

        roles = []
        links = []
        count = {}
        for tuple4 in list(RoleHierarchy.objects.values_list(
                'role_type_a', 'role_id_a', 'role_type_b', 'role_id_b')):
            role_a = ('%s %s' % (tuple4[0], tuple4[1])) if tuple4[1] else tuple4[0]  # noqa
            role_b = (('%s %s' % (tuple4[2], tuple4[3])) if tuple4[3] else tuple4[2])  # noqa
            if role_a not in count:
                count[role_a] = 1
                roles.append(role_a)
            else:
                count[role_a] += 1
            if role_b not in count:
                count[role_b] = 1
                roles.append(role_b)
            else:
                count[role_b] += 1
            # I think we can add scores on links
            links.append({'source': roles.index(role_b),
                          'target': roles.index(role_a)})

        # possible types: circle, square, triangle-up/down, diamond, cross
        data = {
            'directed': True,
            'multigraph': False,
            'links': links,
            'nodes': [
                {'size': min(count[r], 50), 'score': min(count[r] / 100, 1),
                 'id': r if ' ' not in r else str(
                     app_settings.mapping.get_instance(*r.split(' '))),
                 'type': {
                     # FIXME: put this outside of cerberus: it's genida related
                     'member': 'circle',
                     'relative': 'square',
                     'cohort': 'diamond',
                     'gene': 'cross',
                     'copy_number_variant': 'cross',
                 }.get(r.split(' ')[0], 'triangle-down')}
                for r in roles
            ]
        }

        self.grid = Grid(Row(Column(Box(
            title='Role Hierarchy Graph',
            template='cerberus_ac/view_role_hierarchy.html',
            context=json.dumps(data)))))

        return super(ViewRoleHierarchy, self).get(request, *args, **kwargs)


# Ajax views ------------------------------------------------------------------
def ajax_edit_privileges(request,
                         role_type,
                         resource_type,
                         role_id,
                         resource_id,
                         privilege,
                         action):
    user = request.user
    success = False

    if not request.is_ajax():
        return bad_request(request, ValueError('not an ajax request'))
    elif not user.can('update', 'role_privilege'):
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


def ajax_load_roles_and_resources(request, role_type, resource_type):
    if not request.is_ajax():
        return bad_request(request, ValueError('not an ajax request'))

    role_class = app_settings.mapping.get_class(role_type)
    resource_class = app_settings.mapping.get_class(resource_type)

    role_instances = role_class.objects.order_by('id')
    resource_instances = resource_class.objects.order_by('id')

    role_instances = [(r.id, str(r)) for r in role_instances]
    resource_instances = [(r.id, str(r)) for r in resource_instances]

    data = {'roles': role_instances, 'resources': resource_instances}

    return HttpResponse(json.dumps(data), content_type="application/json")


def ajax_load_privileges(request, role_type, role_id, resource_type):
    if not request.is_ajax():
        return bad_request(request, ValueError('not an ajax request'))

    resource_class = app_settings.mapping.get_class(resource_type)
    resource_instances = resource_class.objects.order_by('id')

    default_access_types = ('read', 'update', 'delete')

    data = []

    for resource in resource_instances:
        current_privileges = {}
        db_access_types = []
        for privilege in RolePrivilege.objects.filter(
                role_type=role_type, role_id=role_id,
                resource_type=resource_type, resource_id=resource.id):
            current_privileges[privilege.access_type] = privilege.authorized
            db_access_types.append(privilege.access_type)
        for default_access_type in default_access_types:
            if default_access_type not in db_access_types:
                current_privileges[default_access_type] = None
        data.append(current_privileges)

    return HttpResponse(json.dumps(data), content_type="application/json")
