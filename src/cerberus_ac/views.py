from django.shortcuts import render
from suit_dashboard.views import DashboardView
from suit_dashboard.layout import Grid, Row, Column, Box

from . import AppSettings

resources_list = AppSettings.get_actual_ressources_classes()
role_classes = AppSettings.get_actual_role_classes()

def edituserpermpost(request, user):
    if request.method == "POST":
        pass


class Edituserperm(DashboardView):
    role_instances = []
    for r in role_classes :
        role_instances.extend(r.objects.all())

    resources_real_list = []
    for res in resources_list :
        resources_real_list.extend(res.objects.all())

    grid = Grid(Row(Column(
        Box(template='cerberus_ac/edit_user_perms.html',
            context={'members': role_instances, 'resources': resources_real_list})
    )))


def editgrouppermpost(request, user):
    if request.method == "POST":
        pass



class Editgroupperm(DashboardView):
    role_instances = []
    for r in role_classes:
        role_instances.extend(r.objects.all())

    resources_real_list = []
    for res in resources_list:
        resources_real_list.extend(res.objects.all())

    grid = Grid(Row(Column(
        Box(template='cerberus_ac/edit_user_perms.html',
            context={'members': role_instances, 'resources': resources_real_list})
    )))

