from django.conf.urls import url

from . import views

app_name = 'poolowner'
urlpatterns = [
    url(r'^(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),

    url(r'^(?P<groupowner_id>[0-9]+)/(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'index'),
    url(r'^(?P<groupowner_id>[0-9]+)(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),
    url(r'^(?P<filter>[0-9]+)/(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),

    url(r'^(?P<groupowner_id>[0-9]+)/$', views.index.as_view(), name = 'index'),
    url(r'^(?P<filter>[0-9]+)/$', views.index.as_view(), name = 'index'), 
    url(r'^(?P<modelstate>.*)/$', views.index.as_view(), name = 'index'),

    url(r'^(?P<modelstate>.*)$', views.index.as_view(), name ='index'),
    url(r'^$', views.index.as_view(), name ='index'),

]