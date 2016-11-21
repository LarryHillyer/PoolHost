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
from poolgroup.viewmodels import SuperUser_Index, GroupOwner_Index, SuperUser_Create, SuperUser_Edit


class index(View):

    title = 'Pool Group - Index'
    template_name = 'app/shared_index_pagination.html'

    def get(self, request, groupowner_id = 0, filter = 0, modelstate = None ):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, modelstate, groupowner_id, filter)
        else:
            viewmodel = GroupOwner_Index.get_index_viewmodel(site_user,self.title, modelstate, groupowner_id, filter)
        
        return render(request, self.template_name, viewmodel)

class create(View):

    title = 'Pool Group - Create'
    template_name = 'app/shared_create.html'
    form_class = PoolGroupForm

    def get(self,request, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        form = self.form_class()
        if site_user.is_superuser == True:
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, modelstate, groupowner_id, filter)
        else:
            #view_model = GroupOwner_Create.get_index_viewmodel(site_user,self.title, modelstate, groupowner_id, filter)
            pass

        if viewmodel['modelstate'].split(':')[0] == 'Error':
            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                        kwargs = {'modelstate':viewmodel['modelstate']}))
        return render(request, self.template_name, viewmodel)

    def post(self, request, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        form = self.form_class(request.POST)
        if site_user.is_groupowner and site_user.is_superuser != True:
            groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id)
            form.data.groupowner_id = groupowner_id
       
        if form.is_valid():
            same_poolgroup = PoolGroup.get_item_by_name(PoolGroup, form.data['name'])
        
            if same_poolgroup != None:
                modelstate = 'Error: Pool Group, ' + same_poolgroup.name + ' has already been taken!'
                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, 
                    modelstate, groupowner_id, filter)
                render(request, self.template_name, viewmodel)
            
            poolgroup = PoolGroup(name = form.data['name'], groupowner_id = form.data['groupowner_id'])
            modelstate = PoolGroup.add_item(PoolGroup, poolgroup)
            return HttpResponseRedirect(reverse('poolgroup:index', args = (),
                                                kwargs = {'modelstate': modelstate}))
        else:
            modelstate = 'Error: Invalid Input!' 
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, 
                modelstate, groupowner_id, filter)
            render(request, self.template_name, viewmodel)

class edit(View):
    title = 'Pool Group - Create'
    template_name = 'app/shared_create.html'
    form_class = PoolGroupForm

    def get(self, request, poolgroup_id = None, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, self.form_class, modelstate, poolgroup_id, groupowner_id, filter)
        else:
            #view_model = GroupOwner_Create.get_index_viewmodel(site_user,self.title, modelstate, groupowner_id, filter)
            pass

        if viewmodel['modelstate'].split(':')[0] == 'Error':
            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                        kwargs = {'modelstate':viewmodel['modelstate']}))
        return render(request, self.template_name, viewmodel)

class details(View):

    def get(self,request, poolgroup_id = None, groupowner_id = 0, filter = 0,):
        pass

class delete(View):

    def get(self,request, poolgroup_id = None, groupowner_id = 0, filter = 0,):
        pass

