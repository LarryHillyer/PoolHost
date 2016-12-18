from django.conf.urls import url

from . import views

app_name = 'division'
urlpatterns = [

    url(r'^edit/(?P<division_id>[0-9]+)/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.edit.as_view(), name = 'edit'),
    url(r'^edit/(?P<division_id>[0-9]+)/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.edit.as_view(), name = 'edit'),

    url(r'^delete/(?P<division_id>[0-9]+)/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.delete.as_view(), name = 'delete'),
    url(r'^delete/(?P<division_id>[0-9]+)/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.delete.as_view(), name = 'delete'),

    url(r'^details/(?P<division_id>[0-9]+)/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.details.as_view(), name = 'details'),
    url(r'^details/(?P<division_id>[0-9]+)/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.details.as_view(), name = 'details'),
  
    url(r'^create/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.create.as_view(), name = 'create'),
    url(r'^create/(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.create.as_view(), name = 'create'),

    url(r'^(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),
    url(r'^(?P<conference_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'index'),
    url(r'^$', views.index.as_view(), name = 'index'),

]
