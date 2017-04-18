# -*- coding: utf-8 -*-

"""Utils module."""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


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
