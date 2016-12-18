from django.conf.urls import url

from . import views

app_name = 'league'
urlpatterns = [

    url(r'^delete/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.delete.as_view(), name = 'delete'),
    url(r'^delete/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.delete.as_view(), name = 'delete'),

    url(r'^details/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.details.as_view(), name = 'details'),
    url(r'^details/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.details.as_view(), name = 'details'),

    url(r'^edit/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.edit.as_view(), name = 'edit'),
    url(r'^edit/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.edit.as_view(), name = 'edit'),
  
    url(r'^create/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.create.as_view(), name = 'create'),
    url(r'^create/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.create.as_view(), name = 'create'),

    url(r'^(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),
    url(r'^(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'index'),

    url(r'^redirect/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.league_redirect.as_view(), name = 'redirect'),
    url(r'^redirect/(?P<league_id>[0-9]+)/(?P<sport_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.league_redirect.as_view(), name = 'redirect'),

    url(r'^redirect/(?P<league_id>[0-9]+)/$', views.league_redirect.as_view(), name = 'redirect'),

]

