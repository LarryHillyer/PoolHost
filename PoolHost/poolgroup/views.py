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

from poolgroup.viewmodels import SuperUser_Index,  SuperUser_Create, SuperUser_Edit, SuperUser_Transfer, SuperUser_Details
from poolgroup.viewmodels import GroupOwner_Index, GroupOwner_Create, GroupOwner_Edit, GroupOwner_Details
from poolgroup.viewmodels import User_Delete

from poolgroup.forms import PoolGroupForm_SuperUser_Create, PoolGroupForm_SuperUser_Edit, PoolGroupForm_SuperUser_Transfer
from poolgroup.forms import PoolGroupForm_GroupOwner_Create, PoolGroupForm_GroupOwner_Edit

class index(View):

    title = 'Pool Group - Index'
    template_name = 'app/shared_index_pagination.html'

    def get(self, request, filter = 0, groupowner_id = 0, modelstate = None ):

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
            viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, modelstate, filter, groupowner_id)
        else:
            viewmodel = GroupOwner_Index.get_index_viewmodel(site_user,self.title, modelstate, filter)
        
        return render(request, self.template_name, viewmodel)

class create(View):

    title = 'Pool Group - Create'
    template_name = 'app/shared_create.html'

    def get(self,request, groupowner_id = 0, filter = 0, modelstate = None):

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
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                modelstate, filter, groupowner_id)
        else:
            viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title,  
                modelstate, filter, groupowner_id)

        if viewmodel['modelstate'].split(':')[0] == 'Error':
            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                        kwargs = {'modelstate':viewmodel['modelstate'],
                                                    'groupowner_id': groupowner_id,
                                                    'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request,  groupowner_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            form = PoolGroupForm_SuperUser_Create(request.POST)
        if site_user.is_groupowner and site_user.is_superuser != True:
            form = PoolGroupForm_GroupOwner_Create(request.POST)
            groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id
            
        if form.is_valid():
            same_poolgroup = PoolGroup.get_same_poolgroup_in_database(form.data['name'], form.data['groupowner_id'])
            if same_poolgroup.count() > 0:
                modelstate = 'Error: Pool Group, ' + same_poolgroup.name + ' has already been taken!'
                if site_user.is_superuser:
                    viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, 
                        modelstate, filter, groupowner_id)
                else:
                    viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title, form, 
                        modelstate, filter, groupowner_id)

                render(request, self.template_name, viewmodel)
            
            poolgroup = PoolGroup(name = form.data['name'], groupowner_id = form.data['groupowner_id'])
            modelstate = PoolGroup.add_item(PoolGroup, poolgroup)
            return HttpResponseRedirect(reverse('poolgroup:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'groupowner_id': form.data['groupowner_id'],
                                                            'filter' : form.data['filter']}))

        else:
            modelstate = 'Error: Invalid Input!' 
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, form, 
                modelstate, filter, groupowner_id)
            render(request, self.template_name, viewmodel)

class edit(View):
    title = 'Pool Group - Edit'
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
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, poolgroup_id, filter, groupowner_id)
        else:
            viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user, self.title, modelstate, poolgroup_id, filter, groupowner_id)
            pass

        if viewmodel['modelstate'].split(':')[0] == 'Error':
            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                        kwargs = {'modelstate':viewmodel['modelstate']}))
        return render(request, self.template_name, viewmodel)

    def post(self, request, groupowner_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            form = PoolGroupForm_SuperUser_Edit(request.POST)
        else:
            form = PoolGroupForm_GroupOwner_Edit(request.POST)

        if form.is_valid():

            exactly_same_poolgroup = PoolGroup.get_exactly_same_poolgroup(form.data['id'], 
                form.data['name'], form.data['groupowner_id'])

            if exactly_same_poolgroup.count() > 0:
                modelstate = 'Error: No Changes were made during edit, update aborted!'    
                if site_user.is_superuser:
                    viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, self.form_class,
                         modelstate, poolgroup_id, filter, groupowner_id)
                    render(request, self.template_name, viewmodel)
                else:
                    viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user, self.title, form, 
                        modelstate, filter, groupowner_id)
                    pass

            same_poolgroup = PoolGroup.get_same_poolgroup_in_database(form.data['name'], 
                form.data['groupowner_id']) 

            if same_poolgroup.count() > 0:
                modelstate = 'Error: Poolgroup is already in the database, update aborted!'    
                if site_user.is_superuser:
                    viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, self.form_class,
                         modelstate, poolgroup_id, filter, groupowner_id)
                    render(request, self.template_name, viewmodel)

                else:
                    viewmodel = GroupOwner_Edit.get_create_viewmodel(site_user, self.title, form, 
                        modelstate, filter, groupowner_id)
                    pass

            poolgroup = PoolGroup.get_item_by_id(PoolGroup, form.data['id'])
            poolgroup.name = form.data['name']
            poolgroup.groupowner_id = form.data['groupowner_id']
            modelstate = PoolGroup.edit_item(PoolGroup, poolgroup)
            if modelstate.split(':')[0] != 'Error':
                return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                            kwargs = {'modelstate':modelstate,
                                                        'groupowner_id': form.data['groupowner_id'],
                                                        'filter' : form.data['filter']}))

        else:
            modelstate = 'Error: Invalid Input!' 
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, self.form_class,
                modelstate, poolgroup_id, filter, groupowner_id)
            render(request, self.template_name, viewmodel)
 
class transfer(View):
    title = 'Pool Group - Transfer Ownership'
    form_class = PoolGroupForm_SuperUser_Transfer
    template_name = 'app/shared_create.html'
    
    def get(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        view_model = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, poolgroup_id, groupowner_id, filter, modelstate)

        return render(request, self.template_name, view_model)

    def post(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        form = PoolGroupForm_SuperUser_Transfer(request.POST)
        if form.is_valid():

            poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)               
            if poolgroup.groupowner_id == form.data['groupowner_id']:
                modelstate = 'Error: New groupowner is same as old groupower!'
                view_model = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, groupowner_id, filter, modelstate)
                return render(request, self.template_name, view_model)
            poolgroup = PoolGroup.get_items_by_id(PoolGroup, poolgroup.id)
            modelstate = PoolGroup.transfer_group_ownership(poolgroup, form.data['groupowner_id'], modelstate)
            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                                    kwargs = {'modelstate':modelstate,
                                                                'groupowner_id': form.data['groupowner_id'],
                                                                'filter': filter}))

        else:
            view_model = Transfer_ViewModel.get_transfer_viewmodel(site_user, self.title, groupowner_id, filter, modelstate)
            return render(request, self.template_name, view_model)
  
class details(View):

    title = 'Pool Group - Details'
    template_name = 'app/shared_details.html'

    def get(self,request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

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

        if poolgroup_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser == True:
            viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, modelstate, poolgroup_id, filter,
                groupowner_id)
        else:
            viewmodel = GroupOwner_Details.get_details_viewmodel(site_user,self.title, modelstate, poolgroup_id, filter,
                groupowner_id)
        
        return render(request, self.template_name, viewmodel)
        
class delete(View):

    title = 'Pool Group - Delete'
    template_name = 'app/shared_delete.html'

    def get(self,request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolgroup_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        viewmodel = User_Delete.get_delete_viewmodel(site_user, self.title, 
               modelstate, poolgroup_id, filter, groupowner_id)
        
        return render(request, self.template_name, viewmodel)

    def post(self, request, poolgroup_id = 0, filter = 0, groupowner_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolgroup_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        modelstate = PoolGroup.delete_item(PoolGroup, poolgroup)

        return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                    kwargs = {'modelstate': modelstate,
                                                'groupowner_id': groupowner_id,
                                                'filter': filter}))
