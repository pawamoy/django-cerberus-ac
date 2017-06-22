# -*- coding: utf-8 -*-

"""Utils module."""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .apps import AppSettings

app_settings = AppSettings()


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


def get_role_type(role):
    """
    Get a role's type.

    Args:
        role (obj): a Python object.

    Returns:
        str: the role's type.
    """
    if hasattr(role, 'role_type'):
        attr = role.role_type
        if callable(attr):
            return attr()
        return attr
    return app_settings.mapping.get_type(role)


def get_role_id(role):
    """
    Get a role's ID.

    Args:
        role (obj): a Python object.

    Returns:
        str: the role's ID or None.
    """
    if hasattr(role, 'role_id'):
        attr = role.role_id
        if callable(attr):
            return str(attr())
        return str(attr)
    elif hasattr(role, 'id'):
        return str(role.id)
    return ''


def get_role_type_and_id(role, role_id=''):
    """
    Return both type and ID of a role.

    Args:
        role (obj): string or role instance.
        role_id (str): string ID or None.

    Returns:
        tuple: type and ID of role.
    """
    if isinstance(role, str):
        return role, role_id
    return get_role_type(role), get_role_id(role)


def get_resource_type(resource):
    """
    Get a resource's type.

    Args:
        resource (obj): a Python object.

    Returns:
        str: the resource's type.
    """
    if hasattr(resource, 'resource_type'):
        attr = resource.resource_type
        if callable(attr):
            return attr()
        return attr
    return app_settings.mapping.get_type(resource)


def get_resource_id(resource):
    """
    Get a resource's ID.

    Args:
        resource (obj): a Python object.

    Returns:
        str: the resource's ID or None.
    """
    if hasattr(resource, 'resource_id'):
        attr = resource.resource_id
        if callable(attr):
            return attr()
        return attr
    elif hasattr(resource, 'id'):
        return resource.id
    return None


def get_resource_type_and_id(resource, resource_id=''):
    """
    Return both type and ID of a resource.

    Args:
        resource (obj): string or resource instance.
        resource_id (str): string ID or None.

    Returns:
        tuple: type and ID of resource.
    """
    if isinstance(resource, str):
        return resource, resource_id
    return get_resource_type(resource), get_resource_id(resource)
