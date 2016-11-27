from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import PoolGroup, GroupOwner, SiteUser

class index(View):

    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0):
        pass
