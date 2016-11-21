from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

class index(View):
    def get(self, request):
        pass