from django.conf.urls import url

from . import views

app_name = 'pool'
urlpatterns = [

    url(r'^(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),
    url(r'^(?P<poolowner_id>[0-9]+)/(?P<poolgroup_id>[0-9]+)/(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'index'),

]