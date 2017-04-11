# -*- coding: utf-8 -*-

"""Admin module."""

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .apps import AppSettings
from .models import (
    AccessHistory, PrivilegeHistory, Role, RoleHierarchy, RolePrivilege)


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

# TODO: override save_model methods for history
# https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model


class RoleAdmin(admin.ModelAdmin):
    """Role admin class."""


class RolePrivilegeAdmin(admin.ModelAdmin):
    """Role privilege admin class."""


class RoleHierarchyAdmin(admin.ModelAdmin):
    """Role hierarchy admin class."""

    list_display = ('role_type_a', 'role_id_a', 'role_type_b', 'role_id_b')


class AccessHistoryAdmin(admin.ModelAdmin):
    """Acces history admin class."""

    list_display = (
        'role_type',
        'role_id',
        'response',
        'response_type',
        'access_type',
        'resource_type',
        'resource_id',
        'datetime',
        'conveyor_type',
        'conveyor_id'
    )


class PrivilegeHistoryAdmin(admin.ModelAdmin):
    """Privilege history admin class."""

    list_display = (
        'datetime',
        'user',
        'action',
        'role_type',
        'role_id',
        'role_link',
        'authorized',
        'access_type',
        'resource_type',
        'resource_id',
        'resource_link')

    def role_link(self, obj):
        instance = AppSettings.get_mapping().instance_from_name_and_id(
            obj.resource_type, obj.resource_id)
        info = (instance._meta.app_label, instance._meta.model_name)
        admin_url = reverse('admin:%s_%s_change' % info,
                            args=(instance.pk,))
        return mark_safe('<a href="%s">%s</a>' % (admin_url, instance))
    role_link.short_description = _('Role link')

    def resource_link(self, obj):
        instance = AppSettings.get_mapping().instance_from_name_and_id(
            obj.resource_type, obj.resource_id)
        info = (instance._meta.app_label, instance._meta.model_name)
        admin_url = reverse('admin:%s_%s_change' % info,
                            args=(instance.pk,))
        return mark_safe('<a href="%s">%s</a>' % (admin_url, instance))
    resource_link.short_description = _('Resource link')


# class HierarchyHistoryAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Role, RoleAdmin)
admin.site.register(RolePrivilege, RolePrivilegeAdmin)
admin.site.register(RoleHierarchy, RoleHierarchyAdmin)
admin.site.register(AccessHistory, AccessHistoryAdmin)
admin.site.register(PrivilegeHistory, PrivilegeHistoryAdmin)
# admin.site.register(HierarchyHistory, HierarchyHistoryAdmin)
