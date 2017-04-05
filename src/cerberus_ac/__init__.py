# -*- coding: utf-8 -*-

r"""Cerberus Access Control package."""

import importlib
from django.conf import settings

__version__ = '0.1.3'


def _import(complete_path):
    module_name = '.'.join(complete_path.split('.')[:-1])
    imported_module = importlib.import_module(name=module_name)
    function_or_class = getattr(imported_module, complete_path.split('.')[-1])
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
    MAPPING = {}

    def __init__(self):
        """Load settings in self."""
        self.default_response = AppSettings.get_default_response()
        self.skip_implicit = AppSettings.get_skip_implicit()
        self.log_access = AppSettings.get_log_access()
        self.log_privileges = AppSettings.get_log_privileges()
        self.log_hierarchy = AppSettings.get_log_hierarchy()
        self.mapping = AppSettings.get_mapping()

    @staticmethod
    def check():
        """Run every check method for settings."""
        AppSettings.check_default_response()
        AppSettings.check_skip_implicit()
        AppSettings.check_log_access()
        AppSettings.check_log_privileges()
        AppSettings.check_log_hierarchy()
        AppSettings.check_mapping()

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
    def check_mapping():
        """Check the value of given mapping setting."""
        mapping = getattr(settings, 'CERBERUS_MAPPING', AppSettings.MAPPING)
        if not isinstance(mapping, tuple):
            raise ValueError('MAPPING must be a tuple')
        if not all(isinstance(o, tuple) for o in mapping):
            raise ValueError('MAPPING must be a tuple of (key, value) tuples')
        for k, v in mapping:
            if not isinstance(k, str):
                raise ValueError('Keys in MAPPING must be str')
            if not isinstance(v, dict):
                raise ValueError('Values in MAPPING must be dict')
            if set(v.keys()) != {'name', 'attr'}:
                raise ValueError('Values in MAPPING must be dict '
                                 'with name and attr keys')
        l = [o[1] for o in mapping]
        if len(set([x['name'] for x in l if l.count(x['name']) > 1])) > 0:
            raise ValueError('Names in MAPPING values must be unique')

    @staticmethod
    def get_mapping():
        """Return mapping setting."""
        return Mapping(getattr(
            settings, 'CERBERUS_MAPPING', AppSettings.MAPPING))


class Mapping(object):
    """Mapping class to map roles/resources names to their classes."""

    def __init__(self, mapping):
        """
        Initialization method.

        Args:
            mapping (dict): CERBERUS_MAPPING setting.
        """
        self.mapping = mapping

    def class_from_name(self, name):
        """
        Return the class given the name of a role/resource.

        Args:
            name (str): the type of role/resource.

        Returns:
            class: the corresponding the role/resource class.
        """
        for k, v in self.mapping:
            if v['name'] == name:
                return _import(k)
        return None

    def instance_from_name_and_id(self, name, id):
        """
        Return an instance given a role/resource type and an ID.

        Args:
            name (str): the type of role/resource.
            id (int): an integer or None.

        Returns:
            obj: the instance or a (name, id) tuple if not found.
        """
        cls = self.class_from_name(name)
        if cls:
            if hasattr(cls, 'objects') and id:
                return cls.objects.get(id=id)
            return cls, id
        from .models import Role
        try:
            return Role.objects.get(type=name, rid=id)
        except Role.DoesNotExist:
            return name, id

    def name_from_instance(self, obj):
        """
        Return the type of a role/resource given a Python object.

        Args:
            obj (obj): a Python object.

        Returns:
            str: the role/resource type.
        """
        for k, v in self.mapping:
            # FIXME: use complete path, not just the end
            if k.split('.')[-1] == obj.__class__.__name__:
                return v['name']
        return obj.__class__.__name__

    def user_classes(self):
        """Return the user-role classes."""
        return [_import(k) for k, v in self.mapping
                if 'user' in v['attr'].split()]

    def group_classes(self):
        """Return the group-role classes."""
        return [_import(k) for k, v in self.mapping
                if 'group' in v['attr'].split()]

    def role_types(self):
        """Return the role types."""
        return [v['name'] for k, v in self.mapping
                if len({'user', 'group', 'role'} &
                       set(v['attr'].split())) > 0]

    def role_classes(self):
        """Return the role classes."""
        return [_import(k) for k, v in self.mapping
                if len({'user', 'group', 'role'} &
                       set(v['attr'].split())) > 0]

    def resource_types(self):
        """Return the resource types."""
        return [v['name'] for k, v in self.mapping
                if 'resource' in v['attr'].split()]

    def resource_classes(self):
        """Return the resource classes."""
        return [_import(k) for k, v in self.mapping
                if 'resource' in v['attr'].split()]


AppSettings.check()
