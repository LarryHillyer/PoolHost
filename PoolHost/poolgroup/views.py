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
from poolgroup.viewmodels import SuperUser_Index, GroupOwner_Index

class index(View):

    template_name = 'app/shared_index_pagination.html'

    def get(self, request, groupowner_id = None, filter = None, modelstate = None ):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser == True:
            view_model = SuperUser_Index.get_index_viewmodel(site_user, modelstate, groupowner_id, filter)
        else:
            view_model = GroupOwner_Index.get_index_viewmodel(site_user, modelstate, groupowner_id, filter)
        
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

