from django.conf.urls import url

from . import views

app_name = 'superuser'
urlpatterns = [

    url(r'^create/(?P<modelstate>.*)/$', views.create.as_view(), name = 'create'),
    url(r'^create/$', views.create.as_view(), name ='create'),

    url(r'^delete/(?P<superuser_id>[0-9]+)/$', views.delete.as_view(), name = 'delete'),
    url(r'^details/(?P<superuser_id>[0-9]+)/$', views.details.as_view(), name = 'details'),

    url(r'^(?P<modelstate>.*)$', views.index.as_view(), name ='index'),
    url(r'^$', views.index.as_view(), name ='index'),
]