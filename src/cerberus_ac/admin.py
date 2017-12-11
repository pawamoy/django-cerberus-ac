# -*- coding: utf-8 -*-

"""Admin module."""

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .apps import AppSettings
from .models import (
    AccessHistory, PrivilegeHistory, Role, RoleHierarchy, RolePrivilege)

app_settings = AppSettings()


# class SecurityAdmin(AdminSite):
#     pass
#
#
# class DataAdmin(AdminSite):
#     pass
#
#
# class AuditAdmin(AdminSite):
#     pass
#
#
# security_admin_site = SecurityAdmin(name='SecurityAdmin')
# data_admin_site = DataAdmin(name='DataAdmin')
# audit_admin_site = AuditAdmin(name='AuditAdmin')
#
# Use decorator like @security_admin_site.register(AccessHistory)


def obj_link_generator(type_attr, id_attr, short_description):
    def obj_link(obj):
        obj_type = getattr(obj, type_attr)
        obj_id = getattr(obj, id_attr)
        instance = app_settings.mapping.get_instance(
            obj_type, obj_id)
        if instance is None:
            return '-'
        info = (instance._meta.app_label, instance._meta.model_name)
        admin_url = reverse('admin:%s_%s_change' % info,
                            args=(instance.pk,))
        return format_html('<a href="{}">{}</a>', admin_url, instance)
    obj_link.short_description = short_description
    return obj_link


role_link = obj_link_generator(
    'role_type', 'role_id', _('Role link'))
resource_link = obj_link_generator(
    'resource_type', 'resource_id', _('Resource link'))
hierarchy_role_link_a = obj_link_generator(
    'role_type_a', 'role_id_a', _('Role link A'))
hierarchy_role_link_b = obj_link_generator(
    'role_type_b', 'role_id_b', _('Role link B'))


class RoleAdmin(admin.ModelAdmin):
    """Role admin class."""

    list_display = ('type', 'rid')


class RolePrivilegeAdmin(admin.ModelAdmin):
    """Role privilege admin class."""

    actions_on_top = True
    actions_on_bottom = True

    list_display = (
        '__str__',
        'role_type',
        'role_id',
        role_link,
        'authorized',
        'access_type',
        'resource_type',
        'resource_id',
        resource_link,
        'creation_date',
        'modification_date')

    list_filter = (
        'role_type', 'resource_type', 'authorized', 'access_type',
        'modification_date')
    date_hierarchy = 'creation_date'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        record = PrivilegeHistory(
            user=request.user, action={False: PrivilegeHistory.CREATE}.get(
                change, PrivilegeHistory.UPDATE))
        record.update_from_privilege(obj)


class RoleHierarchyAdmin(admin.ModelAdmin):
    """Role hierarchy admin class."""

    list_display = (
        '__str__',
        'role_type_a',
        'role_id_a',
        hierarchy_role_link_a,
        'role_type_b',
        'role_id_b',
        hierarchy_role_link_b)


class AccessHistoryAdmin(admin.ModelAdmin):
    """Acces history admin class."""

    list_display = (
        'datetime',
        'role_type',
        'role_id',
        role_link,
        'response',
        'response_type',
        'access_type',
        'resource_type',
        resource_link,
        'resource_id',
        'conveyor_type',
        'conveyor_id')


class PrivilegeHistoryAdmin(admin.ModelAdmin):
    """Privilege history admin class."""

    list_display = (
        'datetime',
        'user',
        'action',
        'role_type',
        'role_id',
        role_link,
        'authorized',
        'access_type',
        'resource_type',
        'resource_id',
        resource_link)


# class HierarchyHistoryAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Role, RoleAdmin)
admin.site.register(RolePrivilege, RolePrivilegeAdmin)
admin.site.register(RoleHierarchy, RoleHierarchyAdmin)
admin.site.register(AccessHistory, AccessHistoryAdmin)
admin.site.register(PrivilegeHistory, PrivilegeHistoryAdmin)
# admin.site.register(HierarchyHistory, HierarchyHistoryAdmin)
