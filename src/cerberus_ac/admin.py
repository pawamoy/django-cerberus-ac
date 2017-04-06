# -*- coding: utf-8 -*-

"""Admin module."""

from django.contrib import admin

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


class AccessHistoryAdmin(admin.ModelAdmin):
    """Acces history admin class."""


class PrivilegeHistoryAdmin(admin.ModelAdmin):
    """Privilege history admin class."""


# class HierarchyHistoryAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Role, RoleAdmin)
admin.site.register(RolePrivilege, RolePrivilegeAdmin)
admin.site.register(RoleHierarchy, RoleHierarchyAdmin)
admin.site.register(AccessHistory, AccessHistoryAdmin)
admin.site.register(PrivilegeHistory, PrivilegeHistoryAdmin)
# admin.site.register(HierarchyHistory, HierarchyHistoryAdmin)
