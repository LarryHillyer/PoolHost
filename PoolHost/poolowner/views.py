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

from app.models import Pool, PoolOwner, PoolGroup, PoolGroup_Choices, GroupOwner, SiteUser

from poolowner.viewmodels import SuperUser_Index, SuperUser_Create, SuperUser_Transfer, SuperUser_Details
from poolowner.viewmodels import GroupOwner_Index, GroupOwner_Create, GroupOwner_Transfer, GroupOwner_Details
from poolowner.viewmodels import User_Delete

from poolowner.forms import PoolOwnerForm_Create, PoolOwnerForm_Transfer

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

        '''
        if viewmodel['modelstate'].split(':')[0] == 'Error':
            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                        kwargs = {'modelstate':viewmodel['modelstate'],
                                                    'poolgroup_id': poolgroup_id,
                                                    'groupowner_id': groupowner_id,
                                                    'filter' : filter}))
        '''

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
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(request.POST['groupowner_id'])
            filter = int(request.POST['filter'])

        elif site_user.is_groupowner and not site_user.is_superuser:
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(groupowner_id)
            filter = int(request.POST['filter'])

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)      
        PoolGroup_Choices.get_poolgroup_choices_by_groupowner_id(groupowner_id, poolgroups)

        form = PoolOwnerForm_Create(request.POST)
        
        if form.is_valid():

            poolowner_name_valid = PoolOwner.is_poolowner_siteuser(form.data['name'])

            if poolowner_name_valid:

                poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, form.data['poolgroup_id'])

                poolowners = poolowners.filter(name = form.data['name'])

                if poolowners.count() == 0:
                    new_poolowner = SiteUser.get_item_by_name(SiteUser,form.data['name'])
                    user_id = new_poolowner.user_id
                    SiteUser.make_siteuser_poolowner(new_poolowner)
                    poolowner = PoolOwner(name = form.data['name'], poolgroup_id = form.data['poolgroup_id'], user_id = user_id)
                    modelstate = PoolOwner.add_item(PoolOwner, poolowner)

                    return HttpResponseRedirect(reverse('poolowner:index', args = (),
                                                        kwargs = {'modelstate': modelstate,
                                                                    'poolgroup_id': poolgroup_id,
                                                                    'groupowner_id': groupowner_id,
                                                                    'filter' : filter}))

                else:

                    modelstate = 'Error: Pool Owner, ' + form.data['name'] + ' is already a PoolOwner!!!'

                    return HttpResponseRedirect(reverse('poolowner:create', args = (),
                                                        kwargs = {'modelstate': modelstate,
                                                                    'poolgroup_id': poolgroup_id,
                                                                    'groupowner_id': groupowner_id,
                                                                    'filter' : filter}))
            else:
                modelstate = 'Error: Pool Owner, ' + form.data['name'] + ' is not a vaild site username!'

                return HttpResponseRedirect(reverse('poolowner:create', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter' : filter}))
        
        else:
            modelstate = 'Error: Invalid Data!!! '

            return HttpResponseRedirect(reverse('poolowner:create', args = (),
                                            kwargs = {'modelstate': modelstate,
                                                        'poolgroup_id': poolgroup_id,
                                                        'groupowner_id': groupowner_id,
                                                        'filter' : filter}))
        
class transfer(View):

    title = 'Pool Owner - Transfer'
    template_name = 'app/shared_create.html'

    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)
        else:
            viewmodel = GroupOwner_Transfer.get_transfer_viewmodel(site_user,self.title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('poolowner:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],
                                                            'poolgroup_id': poolgroup_id,
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        old_poolowner_id = int(poolowner_id)
        poolowner_id = int(request.POST['new_poolowner_id'])
        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)
        poolgroup_id = poolowner.poolgroup_id
        groupowner_id = poolowner.poolgroup.groupowner_id
        filter = int(request.POST['filter'])

        form = PoolOwnerForm_Transfer(request.POST)

        if form.is_valid():

            poolowner_pools = Pool.get_items_by_poolowner_id(Pool, old_poolowner_id)               
            modelstate = Pool.transfer_pool_ownership(poolowner_pools, poolowner_id, modelstate)
            return HttpResponseRedirect(reverse('poolowner:index', args=(),
                                                    kwargs = {'modelstate':modelstate,
                                                               'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter': filter}))

        else:
            return HttpResponseRedirect(reverse('poolowner:transfer', args=(),
                                                    kwargs = {'modelstate':modelstate,
                                                                'poolowner_id': poolowner_id,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter': filter}))

class details(View):
    title = 'Pool Owner - Details'
    template_name = 'app/shared_details.html'

    def get(self,request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, 
        filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if poolowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
                modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)
        else:
            viewmodel = GroupOwner_Details.get_details_viewmodel(site_user,self.title, 
                modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)
        
        return render(request, self.template_name, viewmodel)

class delete(View):
    title = 'Pool Owner - Delete'
    template_name = 'app/shared_delete.html'

    def get(self,request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        viewmodel = User_Delete.get_delete_viewmodel(site_user, self.title, 
               modelstate, filter, poolowner_id, poolgroup_id,  groupowner_id)
        
        return render(request, self.template_name, viewmodel)

    def post(self, request, poolowner_id = 0, poolgroup_id = 0, filter = 0, groupowner_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)
        modelstate = PoolOwner.delete_item(poolowner)

        return HttpResponseRedirect(reverse('poolowner:index', args=(),
                                    kwargs = {'modelstate': modelstate,
                                                'poolgroup_id': poolgroup_id,
                                                'groupowner_id': groupowner_id,
                                                'filter': filter}))

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
        poolgroups = PoolGroup.get_poolgroups_by_groupowner_id_2(groupowner_id)
        return JSONResponse(poolgroups)
    
