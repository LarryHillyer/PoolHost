from django.conf.urls import url

from . import views

app_name = 'poolowner'
urlpatterns = [
    url(r'^transfer/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.transfer.as_view(), name = 'transfer'),
    url(r'^transfer/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.transfer.as_view(), name = 'transfer'),
    url(r'^transfer/(?P<poolowner_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.transfer.as_view(), name = 'transfer'),

    url(r'^delete/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.delete.as_view(), name = 'delete'),
    url(r'^delete/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.delete.as_view(), name = 'delete'),

    url(r'^details/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.details.as_view(), name = 'details'),
    url(r'^details/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.details.as_view(), name = 'details'),

    url(r'^edit/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.edit.as_view(), name = 'edit'),
    url(r'^edit/(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.edit.as_view(), name = 'edit'),
    url(r'^edit/(?P<poolowner_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.edit.as_view(), name = 'edit'),
  
    url(r'^create/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.create.as_view(), name = 'create'),
    url(r'^create/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.create.as_view(), name = 'create'),

    url(r'^(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),
    url(r'^(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'index'),

    url(r'^poolgroups_by_groupowner/$', views.poolgroups_by_groupowner_id.as_view(), name = 'poolgroups_by_groupowner_id'),
]