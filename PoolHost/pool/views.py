from datetime import datetime
import os

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from rest_framework.renderers import JSONRenderer

from app.models import Pool, PoolOwner, PoolGroup, GroupOwner, SiteUser
from app.models import GroupOwner_Choices, PoolGroup_Choices, PoolOwner_Choices
from app.models import CronJob_Choices, PoolType_Choices

from pool.viewmodels import SuperUser_Index, SuperUser_Create, SuperUser_Edit, SuperUser_Transfer, SuperUser_Details
from pool.viewmodels import GroupOwner_Index, GroupOwner_Create, GroupOwner_Edit, GroupOwner_Transfer, GroupOwner_Details
from pool.viewmodels import PoolOwner_Index, PoolOwner_Create, PoolOwner_Edit, PoolOwner_Details
from pool.viewmodels import User_Delete

from pool.forms import PoolForm_Create, PoolForm_Edit, PoolForm_Transfer


class index(View):

    title = 'Pool - Index'
    template_name = 'app/shared_index_pagination.html'

    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True and site_user.is_poolowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser:
            viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)
        elif site_user.is_groupowner and not site_user.is_superuser:
            viewmodel = GroupOwner_Index.get_index_viewmodel(site_user,self.title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)
        else:
            viewmodel = PoolOwner_Index.get_index_viewmodel(site_user,self.title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)      
        return render(request, self.template_name, viewmodel)

class create(View):

    title = 'Pool - Create'
    template_name = 'app/shared_create.html'

    def get(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True and site_user.is_poolowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser:
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)
        elif site_user.is_groupowner and not site_user.is_superuser:
            viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title,  
                modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)
        else:
            viewmodel = PoolOwner_Create.get_create_viewmodel(site_user,self.title,  
                modelstate, filter, poolowner_id, poolgroup_id, groupowner_id)

        return render(request, self.template_name, viewmodel)

    def post(self, request, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True and site_user.is_poolowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            poolowner_id = int(request.POST['poolowner_id'])
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(request.POST['groupowner_id'])
            filter = int(request.POST['filter'])

        elif site_user.is_groupowner and not site_user.is_superuser:
            poolowner_id = int(request.POST['poolowner_id'])
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(groupowner_id)
            filter = int(request.POST['filter'])

        else:
            poolowner_id = int(poolowner_id)
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(groupowner_id)
            filter = int(request.POST['filter'])

        PoolGroup_Choices.get_poolgroup_choices(poolgroup_id)
        PoolOwner_Choices.get_poolowner_choices(poolowner_id)

        form = PoolForm_Create(request.POST)
        
        if form.is_valid():

            same_pool = Pool.get_same_pool_in_database(form.data['name'])

            if same_pool == None:

                if int(form.data['cronjob_id']) == -1:
                    cronjob_id = None
                else:
                    cronjob_id = int(form.data['cronjob_id'])

                pool = Pool(name = form.data['name'],
                            cronjob_id = cronjob_id,
                            pooltype_id = int(form.data['pooltype_id']),
                            poolgroup_id = poolgroup_id,
                            poolowner_id = poolowner_id)


                modelstate = Pool.add_item(Pool, pool)

                if modelstate.split(':')[0] != 'Success':
                    return HttpResponseRedirect(reverse('pool:create', args=(),
                                                kwargs = {'modelstate':modelstate,
                                                            'poolowner_id': poolowner_id,
                                                            'poolgroup_id': poolgroup_id,
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : filter}))

                return HttpResponseRedirect(reverse('pool:index', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'poolowner_id': poolowner_id,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter' : filter}))
            else:
                modelstate = 'Error: Pool, ' + form.data['name'] + ' has already been taken!'
                
                return HttpResponseRedirect(reverse('pool:create', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'poolowner_id': poolowner_id,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter' : filter}))
        
        else:
            modelstate = 'Error: Invalid Data!!! '

            return HttpResponseRedirect(reverse('pool:create', args = (),
                                            kwargs = {'modelstate': modelstate,
                                                        'poolowner_id': poolowner_id,
                                                        'poolgroup_id': poolgroup_id,
                                                        'groupowner_id': groupowner_id,
                                                        'filter' : filter}))

class edit(View):
    title = 'Pool - Edit'
    template_name = 'app/shared_create.html'

    def get(self, request, pool_id = 0, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True and site_user.is_poolowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pool_id = int(pool_id)
        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser:
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate,  filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)
        elif site_user.is_groupowner and not site_user.is_superuser:
            viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user, self.title, modelstate,  filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)
        else:
            viewmodel = PoolOwner_Edit.get_edit_viewmodel(site_user, self.title, modelstate,  filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)

        return render(request, self.template_name, viewmodel)

    def post(self, request,  pool_id = 0, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if  not site_user.is_superuser and not site_user.is_groupowner and not site_user.is_poolowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            poolowner_id = int(request.POST['poolowner_id'])
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(request.POST['groupowner_id'])
            filter = int(request.POST['filter'])

        elif site_user.is_groupowner and not site_user.is_superuser:
            poolowner_id = int(request.POST['poolowner_id'])
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(groupowner_id)
            filter = int(request.POST['filter'])

        else:
            poolowner_id = int(poolowner_id)
            poolgroup_id = int(request.POST['poolgroup_id'])       
            groupowner_id = int(groupowner_id)
            filter = int(request.POST['filter'])

        PoolGroup_Choices.get_poolgroup_choices(poolgroup_id)
        PoolOwner_Choices.get_poolowner_choices(poolowner_id)

        form = PoolForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_pool = Pool.get_exactly_same_pool(pool_id, 
                form.data['name'], int(form.data['cronjob_id']), int(form.data['pooltype_id']), poolgroup_id, poolowner_id)

            if exactly_same_pool.count() > 0:

                modelstate = 'Error: No Changes were made during edit, update aborted!'

                return HttpResponseRedirect(reverse('poolgroup:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter' : filter}))

            same_pool = Pool.get_same_pool_in_database(form.data['name'], int(form.data['id'])) 

            if same_pool != None:
                modelstate = 'Error: Pool is already in the database, update aborted!'    

                return HttpResponseRedirect(reverse('pool:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'pool_id': pool_id,
                                                                'poolowner_id': poolowner_id,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter' : filter}))

            if int(form.data['cronjob_id']) == -1:
                cronjob_id = None
            else:
                cronjob_id = int(form.data['cronjob_id'])

            pool = Pool.get_item_by_id(Pool, pool_id)
            pool.name = form.data['name']
            pool.cronjob_id = cronjob_id
            pool.pooltype_id = int(form.data['pooltype_id'])
            pool.poolgroup_id = poolgroup_id
            pool.poolowner_id = poolowner_id
            modelstate = Pool.edit_item(Pool, pool)

            if modelstate.split(':')[0] != 'Success':

                return HttpResponseRedirect(reverse('pool:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'pool_id': pool_id,
                                                                'poolowner_id': poolowner_id,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter' : filter}))

            return HttpResponseRedirect(reverse('pool:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'poolowner_id': poolowner_id,
                                                            'poolgroup_id': poolgroup_id,
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : form.data['filter']}))

        else:
            modelstate = 'Error: Invalid Input!'
 
            return HttpResponseRedirect(reverse('pool:edit', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'pool_id': pool_id,
                                                            'poolowner_id': poolowner_id,
                                                            'poolgroup_id': poolgroup_id,
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : filter}))

class transfer(View):
    title = 'Pool - Transfer'
    template_name = 'app/shared_create.html'

    def get(self, request, pool_id = 0, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pool_id = int(pool_id)
        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, modelstate, filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)
        else:
            viewmodel = GroupOwner_Transfer.get_transfer_viewmodel(site_user,self.title, modelstate, filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('poolowner:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],
                                                            'poolgroup_id': poolgroup_id,
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request, pool_id = 0, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if pool_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        pool_id = int(pool_id)
        poolowner_id = int(request.POST['new_poolowner_id'])
        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)
        poolgroup_id = poolowner.poolgroup_id
        groupowner_id = poolowner.poolgroup.groupowner_id
        filter = int(request.POST['filter'])

        form = PoolForm_Transfer(request.POST)

        if form.is_valid():
            poolowner_pool = Pool.get_item_by_id(Pool, pool_id)               
            modelstate = Pool.transfer_pool_ownership_2(poolowner_pool, poolowner_id, modelstate)
            return HttpResponseRedirect(reverse('pool:index', args=(),
                                                    kwargs = {'modelstate':modelstate,
                                                                'poolowner_id': poolowner_id,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter': filter}))

        else:
            return HttpResponseRedirect(reverse('pool:transfer', args=(),
                                                    kwargs = {'modelstate':modelstate,
                                                                'pool_id': pool_id,
                                                                'poolowner_id': poolowner_id,
                                                                'poolgroup_id': poolgroup_id,
                                                                'groupowner_id': groupowner_id,
                                                                'filter': filter}))

class details(View):
    title = 'Pool - Details'
    template_name = 'app/shared_details.html'

    def get(self,request, pool_id = 0, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, 
        filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True and site_user.is_poolowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pool_id = int(pool_id)
        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if pool_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
                modelstate, filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)
        elif site_user.is_groupowner and not site_user.is_superuser:
            viewmodel = GroupOwner_Details.get_details_viewmodel(site_user,self.title, 
                modelstate, filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)
        else:
            viewmodel = PoolOwner_Details.get_details_viewmodel(site_user,self.title, 
                modelstate, filter, pool_id, poolowner_id, poolgroup_id, groupowner_id)
  
        return render(request, self.template_name, viewmodel)

class delete(View):
    title = 'Pool - Delete'
    template_name = 'app/shared_delete.html'

    def get(self,request, pool_id = 0, poolowner_id = 0, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True and site_user.is_poolowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if pool_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pool_id = int(pool_id)
        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        viewmodel = User_Delete.get_delete_viewmodel(site_user, self.title, 
               modelstate, filter, pool_id, poolowner_id, poolgroup_id,  groupowner_id)
        
        return render(request, self.template_name, viewmodel)

    def post(self, request, pool_id = 0, poolowner_id = 0, poolgroup_id = 0, filter = 0, groupowner_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if  not site_user.is_superuser and not site_user.is_groupowner and not site_user.is_poolowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if pool_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pool_id = int(pool_id)
        poolowner_id = int(poolowner_id)
        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        pool = Pool.get_item_by_id(Pool, pool_id)

        modelstate = Pool.delete_item(Pool, pool)

        return HttpResponseRedirect(reverse('pool:index', args=(),
                                    kwargs = {'modelstate': modelstate,
                                                'poolowner_id': poolowner_id,
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
        poolgroups = PoolGroup.get_poolgroups_with_poolowners_by_groupowner_id(groupowner_id)
        return JSONResponse(poolgroups)

class poolowners_by_poolgroup_id(View):

    def get(self,request): 

        poolgroup_id = int(request.GET['poolgroup_id'])

        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
            if site_user.is_superuser or site_user.is_groupowner:
                poolowners = PoolOwner.get_poolowners_by_poolgroup_id(poolgroup_id)
            else:
                poolowners = PoolOwner.get_poolowner_by_poolgroup_id_and_name(poolgroup_id, site_user.name)
        else:
            poolowners = []
        return JSONResponse(poolowners)

