# -*- coding: utf-8 -*-

"""Admin module."""

from django.contrib import admin
from django.contrib.admin.sites import AdminSite

class SecurityAdmin(AdminSite):
    pass

class DataAdmin(AdminSite):
    pass

class AuditAdmin(AdminSite):
    pass

security_admin_site = SecurityAdmin(name='SecurityAdmin')
data_admin_site = DataAdmin(name='DataAdmin')
audit_admin_site = AuditAdmin(name='AuditAdmin')

