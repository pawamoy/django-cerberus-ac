from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^permissions/edit/$', views.editperm, name='edit_permissions'),
    url(r'^permissions/view/$', views.viewperm, name='view_permissions'),
    url(r'^member_info/$', views.memberinfo, name='view_member_info'),
    url(r'^logs/object_access/$', views.logs_access, name='logs_access'),
    url(r'^logs/permission_changes/$', views.perm_changes, name='perm_changes'),
]