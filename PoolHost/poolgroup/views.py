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

from poolgroup.forms import PoolGroupForm_Create, PoolGroupForm_Edit, PoolGroupForm_Transfer

class index(View):

    title = 'Pool Group - Index'
    template_name = 'app/shared_index_view.html'

    def get(self, request, filter = 0, groupowner_id = 0, modelstate = None ):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and  not site_user.is_groupowner:
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
    template_name = 'app/shared_form_view.html'

    def get(self,request, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_groupowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner_id = int(groupowner_id)
        filter = int(filter)
        form = None

        if site_user.is_superuser:
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                modelstate, filter, groupowner_id, form)
        else:
            viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title,  
                modelstate, filter, groupowner_id, form)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('poolgroup:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request,  groupowner_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_groupowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:    
            groupowner_id = int(request.POST['groupowner_id'])
            filter = int(request.POST['filter'])

        elif site_user.is_groupowner and not site_user.is_superuser:     
            groupowner_id = int(groupowner_id)
            filter = int(request.POST['filter'])

        form = PoolGroupForm_Create(request.POST)
            
        if form.is_valid():
            same_poolgroup = PoolGroup.get_same_poolgroup_in_database(form.data['name'], groupowner_id)
            if same_poolgroup.count() > 0:
                modelstate = 'Error: Pool Group, ' + form.data['name'] + ' has already been taken!'

                if site_user.is_superuser:
                    viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                        modelstate, filter, groupowner_id, form)

                else:
                    viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title,  
                        modelstate, filter, groupowner_id, form)

                return render(request, self.template_name, viewmodel)
            
            poolgroup = PoolGroup(name = form.data['name'], groupowner_id = groupowner_id)
            modelstate = PoolGroup.add_item(PoolGroup, poolgroup)

            if modelstate.split(':')[0] != 'Success':

                if site_user.is_superuser:
                    viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                        modelstate, filter, groupowner_id, form)

                else:
                    viewmodel = GroupOwner_Create.get_create_viewmodel(site_user,self.title,  
                        modelstate, filter, groupowner_id, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('poolgroup:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : form.data['filter']}))

        else:
            modelstate = 'Error: Invalid Input!' 
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate, filter,
                groupowner_id, form)

            return render(request, self.template_name, viewmodel)

class edit(View):
    title = 'Pool Group - Edit'
    template_name = 'app/shared_form_view.html'

    def get(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_groupowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)
        form = None

        if site_user.is_superuser:
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, filter, poolgroup_id,  groupowner_id, form)
        else:
            viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user, self.title, modelstate,  filter, poolgroup_id, groupowner_id, form)

        return render(request, self.template_name, viewmodel)

    def post(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_groupowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            poolgroup_id = int(request.POST['id'])
            groupowner_id = int(request.POST['groupowner_id'])
            filter = int(request.POST['filter'])

        elif site_user.is_groupowner and not site_user.is_superuser:
            poolgroup_id = int(request.POST['id'])     
            groupowner_id = int(groupowner_id)
            filter = int(request.POST['filter'])

        form = PoolGroupForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_poolgroup = PoolGroup.get_exactly_same_poolgroup(form.data['id'], 
                form.data['name'], groupowner_id)

            if exactly_same_poolgroup.count() > 0:

                modelstate = 'Error: No Changes were made to Pool Group, ' + form.data['name'] + ' update aborted!'

                if site_user.is_superuser:
                    viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                        modelstate, filter, poolgroup_id, groupowner_id, form)

                else:
                    viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user,self.title,  
                        modelstate, filter, poolgroup_id, groupowner_id, form)

                return render(request, self.template_name, viewmodel)
   
            same_poolgroup = PoolGroup.get_same_poolgroup_in_database(form.data['name'], 
                groupowner_id) 

            if same_poolgroup.count() > 0:
                modelstate = 'Error: Poolgroup, ' + form.data['name'] + ' is already in the database, update aborted!'    

                if site_user.is_superuser:
                    viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                        modelstate, filter,  poolgroup_id, groupowner_id, form)

                else:
                    viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user,self.title,  
                        modelstate, filter, poolgroup_id, groupowner_id, form)

                return render(request, self.template_name, viewmodel)

            poolgroup = PoolGroup.get_item_by_id(PoolGroup, form.data['id'])
            poolgroup.name = form.data['name']
            poolgroup.groupowner_id = groupowner_id
            modelstate = PoolGroup.edit_item(PoolGroup, poolgroup)

            if modelstate.split(':')[0] != 'Success':

                if site_user.is_superuser:
                    viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                        modelstate, filter, poolgroup_id, groupowner_id, form)

                else:
                    viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user,self.title,  
                        modelstate, filter, poolgroup_id, groupowner_id, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('poolgroup:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : form.data['filter']}))

        else:
            modelstate = 'Error: Invalid Input!'

            if site_user.is_superuser:
                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, filter, poolgroup_id, groupowner_id, form)

            else:
                viewmodel = GroupOwner_Edit.get_edit_viewmodel(site_user,self.title,  
                    modelstate, filter, poolgroup_id, groupowner_id, form)

            return render(request, self.template_name, viewmodel)
 
class transfer(View):
    title = 'Pool Group - Transfer Ownership'
    template_name = 'app/shared_form_view.html'
    
    def get(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        form = None

        viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, modelstate, filter, poolgroup_id, 
            groupowner_id, form)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('poolgroup:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],
                                                            'groupowner_id': groupowner_id,
                                                            'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolgroup_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(request.POST['filter'])

        form = PoolGroupForm_Transfer(request.POST)

        if form.is_valid():

            poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)
              
            if form.data['new_groupowner_id'] == poolgroup.groupowner_id:

                modelstate = 'Error: New groupowner is same as old groupower!'

                viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, modelstate, 
                    filter, poolgroup_id, groupowner_id, form)

                return render(request, self.template_name, viewmodel)

            modelstate = PoolGroup.transfer_group_ownership([poolgroup], form.data['new_groupowner_id'], modelstate)

            if modelstate.split(':')[0] != 'Success':

                viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, modelstate, 
                    filter, poolgroup_id, groupowner_id, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                            kwargs = {'modelstate':modelstate,
                                                        'groupowner_id': form.data['new_groupowner_id'],
                                                        'filter': form.data['filter']}))

        else:

            modelstate = 'Error: Invalid form'

            viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, modelstate, 
                filter, poolgroup_id, groupowner_id, form)

            return render(request, self.template_name, viewmodel)
  
class details(View):

    title = 'Pool Group - Details'
    template_name = 'app/shared_details_view.html'

    def get(self,request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_groupowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        if poolgroup_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser:
            viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, modelstate, filter, poolgroup_id,
                groupowner_id)
        else:
            viewmodel = GroupOwner_Details.get_details_viewmodel(site_user,self.title, modelstate, filter, poolgroup_id,
                groupowner_id)
        
        return render(request, self.template_name, viewmodel)
        
class delete(View):

    title = 'Pool Group - Delete'
    template_name = 'app/shared_delete_view.html'

    def get(self,request, poolgroup_id = 0, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_groupowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolgroup_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        viewmodel = User_Delete.get_delete_viewmodel(site_user, self.title, 
               modelstate, filter, poolgroup_id, groupowner_id)
        
        return render(request, self.template_name, viewmodel)

    def post(self, request, poolgroup_id = 0, filter = 0, groupowner_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_groupowner:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if poolgroup_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        poolgroup_id = int(poolgroup_id)
        groupowner_id = int(groupowner_id)
        filter = int(filter)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)
        modelstate = PoolGroup.delete_item(poolgroup)

        return HttpResponseRedirect(reverse('poolgroup:index', args=(),
                                    kwargs = {'modelstate': modelstate,
                                                'groupowner_id': groupowner_id,
                                                'filter': filter}))
