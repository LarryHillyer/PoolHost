from django.conf.urls import url

from . import views

app_name = 'groupowner'
urlpatterns = [

    url(r'^create/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.create.as_view(), name = 'create'),
    url(r'^create/(?P<filter>[0-9]+)/$', views.create.as_view(), name = 'create'),

    url(r'^delete/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.delete.as_view(), name = 'delete'),
    url(r'^details/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.details.as_view(), name = 'details'),

    url(r'^(?P<filter>[0-9]+)/(?P<modelstate>.*)$', views.index.as_view(), name ='index'),
    url(r'^(?P<filter>[0-9]+)/$', views.index.as_view(), name ='index'),
]

#   url(r'^create/$', views.create.as_view(), name ='create'),
#   url(r'^$', views.index.as_view(), name ='index'),
