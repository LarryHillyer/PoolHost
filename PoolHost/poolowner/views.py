from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from rest_framework.renderers import JSONRenderer


from app.models import PoolOwner, PoolGroup, GroupOwner, SiteUser

from poolowner.viewmodels import SuperUser_Index, SuperUser_Create
#from poolowner.viewmodels import SuperUser_Index,  SuperUser_Create, SuperUser_Edit, SuperUser_Transfer, SuperUser_Details
#from poolowner.viewmodels import GroupOwner_Index, GroupOwner_Create, GroupOwner_Edit, GroupOwner_Details
#from poolowner.viewmodels import User_Delete

from poolowner.forms import PoolOwnerForm_SuperUser_Create, PoolOwnerForm_SuperUser_Edit, PoolOwnerForm_SuperUser_Transfer
from poolowner.forms import PoolOwnerForm_GroupOwner_Create, PoolOwnerForm_GroupOwner_Edit

class index(View):

    title = 'Pool Owner - Index'
    template_name = 'app/shared_index_pagination.html'

    def get(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, modelstate, filter, poolgroup_id, groupowner_id)
        else:
            viewmodel = GroupOwner_Index.get_index_viewmodel(site_user,self.title, modelstate, filter, poolgroup_id)
        
        return render(request, self.template_name, viewmodel)

class create(View):

    title = 'Pool Owner - Create'
    template_name = 'app/shared_create.html'

    def get(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                modelstate, filter, poolgroup_id, groupowner_id)
        else:
            viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title,  
                modelstate, filter, poolgroup_id, groupowner_id)

        if viewmodel['modelstate'].split(':')[0] == 'Error':
            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                        kwargs = {'modelstate':viewmodel['modelstate'],
                                                    'poolgroup_id': poolgroup_id,
                                                    'groupowner_id': groupowner_id,
                                                    'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            form = PoolOwnerForm_SuperUser_Create(request.POST)
        if site_user.is_groupowner and site_user.is_superuser != True:
            form = PoolOwnerForm_GroupOwner_Create(request.POST)
            groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id
        
        if form.is_valid():
            poolowner_name_valid = PoolOwner.is_poolowner_siteuser(form.data['name'])
            if poolowner_name_valid:
                poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, form.data['poolgroup_id'])
                if poolowners.count() == 0:
                    user_id = SiteUser.get_item_by_name(SiteUser,form.data['name']).user_id
                    poolowner = PoolOwner(name = form.data['name'], poolgroup_id = form.data['poolgroup_id'], user_id = user_id)
                    modelstate = PoolOwner.add_item(PoolOwner, poolowner)
                    return HttpResponseRedirect(reverse('poolowner:index', args = (),
                                                        kwargs = {'modelstate': modelstate,
                                                                    'poolgroup_id': form.data['poolgroup_id'],
                                                                    'groupowner_id': form.data['groupowner_id'],
                                                                    'filter' : form.data['filter']}))

                else:
                    modelstate = 'Error: Pool Owner, ' + form.data['name'] + ' is already a PoolOwner!!!'
                    if site_user.is_superuser:
                        viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, 
                            modelstate, filter, groupowner_id)
                    else:
                        viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title, form, 
                            modelstate, filter, groupowner_id)

                    render(request, self.template_name, viewmodel)
            else:
                modelstate = 'Error: Pool Owner, ' + form.data['name'] + ' is not a vaild site username!'
                if site_user.is_superuser:
                    viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, 
                        modelstate, filter, groupowner_id)
                else:
                    viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title, form, 
                        modelstate, filter, groupowner_id)

                render(request, self.template_name, viewmodel)
        
        else:
            modelstate = 'Error: Invalid Data!!! '
            if site_user.is_superuser:
                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, 
                    modelstate, filter, groupowner_id)
            else:
                viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title, form, 
                    modelstate, filter, groupowner_id)

            render(request, self.template_name, viewmodel)
        
class edit(View):
    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0):
        pass

class transfer(View):
    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0):
        pass

class details(View):
    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0):
        pass

class delete(View):
    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0):
        pass

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class poolgroups_by_groupowner_id(View):

    def get(self,request):

        groupowner_id = int(request.GET['groupowner_id'])
        poolgroups = PoolGroup.get_poolgroups_by_groupowner_id(groupowner_id)
        return JSONResponse(poolgroups)
    
