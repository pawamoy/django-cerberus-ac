# -*- coding: utf-8 -*-

"""App module providing the application settings class."""

import importlib

from django.apps import AppConfig

import appsettings as aps


class CerberusACConfig(AppConfig):
    name = 'cerberus_ac'
    verbose_name = 'Cerberus AC'

    def ready(self):
        AppSettings.check()


def _import(complete_path):
    module_name = '.'.join(complete_path.split('.')[:-1])
    imported_module = importlib.import_module(name=module_name)
    function_or_class = getattr(imported_module, complete_path.split('.')[-1])
    return function_or_class


class Mapping(object):
    """Mapping class to map roles/resources names to their classes."""

    def __init__(self, mapping):
        """
        Initialization method.

        Args:
            mapping (dict): CERBERUS_MAPPING setting.
        """
        self.mapping = mapping

    def get_class(self, name):
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

    def get_instance(self, name, id):
        """
        Return an instance given a role/resource type and an ID.

        Args:
            name (str): the type of role/resource.
            id (int): an integer or None.

        Returns:
            obj: the instance or a (name, id) tuple if not found.
        """
        cls = self.get_class(name)
        if cls:
            if hasattr(cls, 'objects') and id:
                try:
                    return cls.objects.get(id=id)
                except (cls.DoesNotExist, ValueError):
                    return None
            return None
        from .models import Role
        try:
            return Role.objects.get(type=name, rid=id)
        except Role.DoesNotExist:
            return None

    def get_type(self, obj):
        """
        Return the type of a role/resource given a Python object.

        Args:
            obj (obj): a Python object (class are accepted).

        Returns:
            str: the role/resource type.
        """
        if isinstance(obj, type):
            class_name = obj.__name__
        else:
            class_name = obj.__class__.__name__
        for k, v in self.mapping:
            # FIXME: use complete path, not just the end
            if k.split('.')[-1] == class_name:
                return v['name']
        return class_name

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


class MappingSetting(aps.Setting):
    def checker(self, name, value):
        """Check the value of given mapping setting."""
        if not isinstance(value, tuple):
            raise ValueError('%s must be a tuple' % name)
        if not all(isinstance(o, tuple) for o in value):
            raise ValueError(
                '%s must be a tuple of (key, value) tuples' % name)
        for k, v in value:
            if not isinstance(k, str):
                raise ValueError('Keys in %s must be str' % name)
            if not isinstance(v, dict):
                raise ValueError('Values in %s must be dict' % name)
            if set(v.keys()) != {'name', 'attr'}:
                raise ValueError('Values in %s must be dict '
                                 'with name and attr keys' % name)
        _ = [o[1] for o in value]
        if {x['name'] for x in _ if _.count(x['name']) > 1}:
            raise ValueError(
                'Names in %s values must be unique' % name)

    def transform(self, value):
        return Mapping(value)


class AppSettings(aps.AppSettings):
    """
    Application settings class.

    Settings:
    - default_response (bool):
    - skip_implicit (bool):
    - log_access (bool):
    - log_privileges (bool):
    - log_hierarchy (bool):
    - mapping (tuple):
    - namespace (str):
    """

    allow_update_own_privileges = aps.BooleanSetting(default=False)
    default_response = aps.BooleanSetting(default=False)
    skip_implicit = aps.BooleanSetting(default=False)
    log_access = aps.BooleanSetting(default=True)
    log_privileges = aps.BooleanSetting(default=True)
    log_hierarchy = aps.BooleanSetting(default=True)
    namespace = aps.StringSetting(default='')
    mapping = MappingSetting(default=())
    access_permission = aps.StringSetting(default='read')

    class Meta:
        setting_prefix = 'CERBERUS_'
