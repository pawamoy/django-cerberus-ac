#! -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag
def owlright(perm_type, resource_type, resoure_id=None):
    pass  # return an object
