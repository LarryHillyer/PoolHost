from django.conf.urls import url
from django.conf.urls import include

from . import views

app_name = 'nfl'
urlpatterns = [
   
    url(r'^conference/', include('nfl.conference.urls')),
    url(r'^division/', include('nfl.division.urls')),

    url(r'^$', views.home.as_view(), name = 'home'),
    url(r'^(?P<link_id>[0-9]+)/$', views.home.as_view(), name = 'home')

]

