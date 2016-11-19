from django.conf.urls import url

from . import views

app_name = 'groupowner'
urlpatterns = [

    url(r'^create/(?P<modelstate>.*)/$', views.create.as_view(), name = 'groupowner_create'),
    url(r'^create/$', views.create.as_view(), name ='groupowner_create'),

    url(r'^delete/(?P<groupowner_id>[0-9]+)/$', views.delete.as_view(), name = 'groupowner_delete'),
    url(r'^details/(?P<groupowner_id>[0-9]+)/$', views.details.as_view(), name = 'groupowner_details'),

    url(r'^(?P<modelstate>.*)$', views.index.as_view(), name ='groupowner_index'),
    url(r'^$', views.index.as_view(), name ='groupowner_index'),
]