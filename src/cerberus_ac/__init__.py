# -*- coding: utf-8 -*-

r"""Cerberus Access Control package."""

import importlib
from django.conf import settings

__version__ = '0.1.2'


def _import(complete_path):
    module_name = '.'.join(complete_path.split('.')[:-1])
    module = importlib.import_module(name=module_name)
    function_or_class = getattr(module, complete_path.split('.')[-1])
    return function_or_class


class AppSettings(object):
    """
    Application settings class.

    This class provides static getters for each setting, and also an instance
    ``load`` method to load every setting in an instance.
    """

    DEFAULT_RESPONSE = False
    SKIP_IMPLICIT = False
    LOG_ACCESS = True
    LOG_PRIVILEGES = True
    LOG_HIERARCHY = True
    RESOURCES_LIST = []
    ROLES_LIST = []
    MAPPING = []

    def load(self):
        """Load settings in self."""
        self.DEFAULT_RESPONSE = AppSettings.get_default_response()
        self.SKIP_IMPLICIT = AppSettings.get_skip_implicit()
        self.LOG_ACCESS = AppSettings.get_log_access()
        self.LOG_PRIVILEGES = AppSettings.get_log_privileges()
        self.LOG_HIERARCHY = AppSettings.get_log_hierarchy()

    @staticmethod
    def check():
        """Run every check method for settings."""
        AppSettings.check_default_response()
        AppSettings.check_skip_implicit()
        AppSettings.check_log_access()
        AppSettings.check_log_privileges()
        AppSettings.check_log_hierarchy()

    @staticmethod
    def check_default_response():
        """Check the value of given default response setting."""
        default_response = AppSettings.get_default_response()
        if not isinstance(default_response, bool):
            raise ValueError('DEFAULT_RESPONSE must be True or False')

    @staticmethod
    def get_default_response():
        """Return default response setting."""
        return getattr(settings, 'CERBERUS_DEFAULT_RESPONSE',
                       AppSettings.DEFAULT_RESPONSE)

    @staticmethod
    def check_skip_implicit():
        """Check the value of given skip implicit setting."""
        skip_implicit = AppSettings.get_skip_implicit()
        if not isinstance(skip_implicit, bool):
            raise ValueError('SKIP_IMPLICIT must be True or False')

    @staticmethod
    def get_skip_implicit():
        """Return skip implicit setting."""
        return getattr(settings, 'CERBERUS_SKIP_IMPLICIT',
                       AppSettings.SKIP_IMPLICIT)

    @staticmethod
    def check_log_access():
        """Check the value of given log access setting."""
        log_access = AppSettings.get_log_access()
        if not isinstance(log_access, bool):
            raise ValueError('LOG_ACCESS must be True or False')

    @staticmethod
    def get_log_access():
        """Return log access setting."""
        return getattr(settings, 'CERBERUS_LOG_ACCESS',
                       AppSettings.LOG_ACCESS)

    @staticmethod
    def check_log_privileges():
        """Check the value of given log privileges setting."""
        log_privileges = AppSettings.get_log_privileges()
        if not isinstance(log_privileges, bool):
            raise ValueError('LOG_PRIVILEGES must be True or False')

    @staticmethod
    def get_log_privileges():
        """Return log privileges setting."""
        return getattr(settings, 'CERBERUS_LOG_PRIVILEGES',
                       AppSettings.LOG_PRIVILEGES)

    @staticmethod
    def check_log_hierarchy():
        """Check the value of given log hierarchy setting."""
        log_hierarchy = AppSettings.get_log_hierarchy()
        if not isinstance(log_hierarchy, bool):
            raise ValueError('LOG_HIERARCHY must be True or False')

    @staticmethod
    def get_log_hierarchy():
        """Return log hierarchy setting."""
        return getattr(settings, 'CERBERUS_LOG_HIERARCHY',
                       AppSettings.LOG_HIERARCHY)

    @staticmethod
    def check_resources_list():
        """Check the value of given resources list setting."""
        resources_list = AppSettings.get_log_hierarchy()
        if (not isinstance(resources_list, list)
                or not all([isinstance(o, str) for o in resources_list])):
            raise ValueError('RESOURCES_LIST must be a list of strings')

    @staticmethod
    def get_resources_list():
        """Return resources list setting."""
        return getattr(settings, 'CERBERUS_RESOURCES_LIST',
                       AppSettings.RESOURCES_LIST)

    @staticmethod
    def get_actual_resources_classes():
        """Return resources classes."""
        resources_list = AppSettings.get_resources_list()
        actual_resources_classes = [_import(c) for c in resources_list]
        return actual_resources_classes

    @staticmethod
    def check_roles_list():
        """Check the value of given roles list setting."""
        roles_list = AppSettings.get_log_hierarchy()
        if (not isinstance(roles_list, list)
                or not all([isinstance(o, str) for o in roles_list])):
            raise ValueError('ROLES_LIST must be a list of strings')

    @staticmethod
    def get_roles_list():
        """Return roles list setting."""
        return getattr(settings, 'CERBERUS_ROLES_LIST',
                       AppSettings.ROLES_LIST)

    @staticmethod
    def get_actual_roles_classes():
        """Return roles classes."""
        roles_list = AppSettings.get_roles_list()
        actual_roles_classes = [_import(c) for c in roles_list]
        return actual_roles_classes

    @staticmethod
    def check_mapping():
        """Check the value of given mapping setting."""
        mapping = AppSettings.get_mapping()
        if (not isinstance(mapping, list)
                or not all([isinstance(o, tuple) and
                            all([isinstance(oo, str) for oo in o])
                            for o in mapping])):
            raise ValueError('MAPPING must be a list of strings')

    @staticmethod
    def get_mapping():
        """Return mapping setting."""
        return getattr(settings, 'CERBERUS_MAPPING', AppSettings.MAPPING)


AppSettings.check()
