from django.conf.urls import url

from . import views

app_name = 'poolgroup'
urlpatterns = [
    url(r'^create/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.create.as_view(), name = 'poolgroup_create'),

    url(r'^create/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.create.as_view(), name = 'poolgroup_create'),
    url(r'^create/(?P<groupowner_id>[0-9]+)(?P<modelstate>.*)/$', views.create.as_view(), name = 'poolgroup_create'),
    url(r'^create/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.create.as_view(), name = 'poolgroup_create'),

    url(r'^create/(?P<groupowner_id>[0-9]+)/$', views.create.as_view(), name = 'poolgroup_create'),
    url(r'^create/(?P<filter>[0-9]+)/$', views.create.as_view(), name = 'poolgroup_create'), 
    url(r'^create/(?P<modelstate>.*)/$', views.create.as_view(), name = 'poolgroup_create'),
    
    url(r'^create/$', views.create.as_view(), name ='poolgroup_create'),

    url(r'^delete/(?P<poolgroup_id>[0-9]+)/$', views.delete.as_view(), name = 'poolgroup_delete'),
    url(r'^details/(?P<poolgroup_id>[0-9]+)/$', views.details.as_view(), name = 'poolgroup_details'),

    url(r'^(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'poolgroup_index'),

    url(r'^(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'poolgroup_index'),
    url(r'^(?P<groupowner_id>[0-9]+)(?P<modelstate>.*)/$', views.index.as_view(), name = 'poolgroup_index'),
    url(r'^(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'poolgroup_index'),

    url(r'^(?P<groupowner_id>[0-9]+)/$', views.index.as_view(), name = 'poolgroup_index'),
    url(r'^(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'poolgroup_index'), 
    url(r'^(?P<modelstate>.*)/$', views.index.as_view(), name = 'poolgroup_index'),

    url(r'^(?P<modelstate>.*)$', views.index.as_view(), name ='poolgroup_index'),

    url(r'^$', views.index.as_view(), name ='poolgroup_index'),
]