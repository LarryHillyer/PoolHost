from django.conf.urls import url

from . import views

app_name = 'cronjobtype'
urlpatterns = [

    url(r'^create/(?P<modelstate>.*)/$', views.create.as_view(), name = 'create'),
    url(r'^create/$', views.create.as_view(), name ='create'),

    url(r'^edit/(?P<cronjobtype_id>[0-9]+)/(?P<modelstate>.*)/$', views.edit.as_view(), name = 'edit'),
    url(r'^edit/(?P<cronjobtype_id>[0-9]+)/$', views.edit.as_view(), name = 'edit'),

    url(r'^details/(?P<cronjobtype_id>[0-9]+)/(?P<modelstate>.*)/$', views.details.as_view(), name = 'details'),
    url(r'^details/(?P<cronjobtype_id>[0-9]+)/$', views.details.as_view(), name = 'details'),

    url(r'^delete/(?P<cronjobtype_id>[0-9]+)/(?P<modelstate>.*)/$', views.delete.as_view(), name = 'delete'),
    url(r'^delete/(?P<cronjobtype_id>[0-9]+)/$', views.delete.as_view(), name = 'delete'),

    url(r'^(?P<modelstate>.*)$', views.index.as_view(), name ='index'),
    url(r'^$', views.index.as_view(), name ='index'),
]