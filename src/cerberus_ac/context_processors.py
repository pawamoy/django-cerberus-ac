# -*- coding: utf-8 -*-


class OwlRight(object):
    def __init__(self, user):
        self.user = user

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, item):
        pass


def owlright(request):
    return OwlRight(request.user)
