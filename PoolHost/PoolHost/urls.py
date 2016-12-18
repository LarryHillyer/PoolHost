"""
Definition of urls for PoolHost.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
from app.views import register

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),

    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^register$', register.as_view(), name = 'register'),

    url(r'^superuser/', include('superuser.urls')),
    url(r'^groupowner/', include('groupowner.urls')),
    url(r'^pooltype/', include('pooltype.urls')),
    url(r'^cronjobtype/', include('cronjobtype.urls')),
    url(r'^cronjob/', include('cronjob.urls')),
    url(r'^sport/', include('sport.urls')),
    url(r'^league/', include('league.urls')),
    url(r'^nfl/', include('nfl.urls')),


    url(r'^poolgroup/', include('poolgroup.urls')),
    url(r'^poolowner/', include('poolowner.urls')),
    url(r'^pool/', include('pool.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
