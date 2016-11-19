from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from poolgroup.forms import PoolGroupForm
from app.models import PoolGroup, GroupOwner, SiteUser

class index(View):

    template_name = 'app/shared_index_pagination.html'
    #template_name = 'app/shared_index.html'

    def get(self, request, groupowner_id = None, filter = None, modelstate = None ):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser == True:
            view_model = PoolGroup.get_superuser_index_view_model(site_user, modelstate, filter, groupowner_id)
        else:
            view_model = PoolGroup.get_groupowner_index_view_model(site_user, modelstate, poolgroups)
        
        return render(request, self.template_name, view_model)

class create(View):

    def get(self,request):
        pass
 
class details(View):

    def get(self,request):
        pass

class delete(View):

    def get(self,request):
        pass

