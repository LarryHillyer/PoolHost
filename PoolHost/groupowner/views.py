from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import PoolGroup, GroupOwner_Choices, GroupOwner, SiteUser

from groupowner.viewmodels import SuperUser_Index, SuperUser_Create, SuperUser_Transfer, SuperUser_Details, SuperUser_Delete
from groupowner.forms import GroupOwnerForm_Create, GroupOwnerForm_Transfer


class index(View):
    title = 'Group Owner - Index'
    template_name = 'app/shared_index_view.html'
    def get(self, request, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        filter = int(filter)

        viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, 
            modelstate, filter)
        
        return render(request, self.template_name, viewmodel)

class create(View):
    title = 'Group Owner - Create'
    form_class = GroupOwnerForm_Create
    template_name = 'app/shared_form_view.html'

    def get(self, request, filter = 0, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        filter = int(filter)
        form = None

        viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, filter, modelstate, form)

        return render(request, self.template_name, viewmodel)
    
    def post(self, request, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        filter = int(filter)

        form = GroupOwnerForm_Create(request.POST)
        if form.is_valid():

            groupowner = GroupOwner(name = request.POST['name'])

            same_groupowner = GroupOwner.get_items_by_name(GroupOwner, groupowner.name)
            if same_groupowner.count() > 0:

                modelstate = 'Error: groupowner, ' + groupowner.name + ' is already a groupowner!'

                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, filter, 
                    modelstate, form)

                return render(request, self.template_name, viewmodel)
                                
            site_user = SiteUser.get_item_by_name(SiteUser, groupowner.name)          
            if site_user != None:

                site_user = SiteUser.make_siteuser_groupowner(site_user) 
                groupowner.user_id = site_user.user.id
                modelstate = GroupOwner.add_item(GroupOwner, groupowner)

                if modelstate.split(':')[0] != 'Success':

                    viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                        filter, modelstate, form)

                    return render(request, self.template_name, viewmodel)
                
                return HttpResponseRedirect(reverse('groupowner:index', args=(),
                                                    kwargs = {'modelstate':modelstate,
                                                                'filter': filter}))
            else:
                modelstate = 'Error: groupowner, ' + groupowner.name + ' is not in database!'

                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, filter, 
                    modelstate, form)

                return render(request, self.template_name, viewmodel)
        else:
            modelstate = 'Error: Nonvalid form!!'

            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, filter, 
                modelstate, form)

            return render(request, self.template_name, viewmodel)

class transfer(View):
    title = 'Group Owner - Transfer Ownership'
    template_name = 'app/shared_form_view.html'

    def get(self, request, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        groupowner_id = int(groupowner_id)
        filter = int(filter)

        form = None
        viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, groupowner_id, filter, 
            modelstate, form)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('groupowner:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],
                                                            'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')            

        groupowner_id = int(groupowner_id)
        filter = int(filter)

        form = GroupOwnerForm_Transfer(request.POST)
        if form.is_valid():

            if form.data['new_groupowner_id'] == groupowner_id:
                modelstate = 'Error: New groupowner is same as old groupower!'
                view_model = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, groupowner_id, filter, modelstate, form)
                return render(request, self.template_name, view_model)

            groupowner_poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)               
            modelstate = PoolGroup.transfer_group_ownership(groupowner_poolgroups, int(form.data['new_groupowner_id']), modelstate)

            if modelstate.split(':')[0] != 'Success':
                view_model = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, filter, modelstate, form)
                return render(request, self.template_name, view_model)
 
            return HttpResponseRedirect(reverse('groupowner:index', args=(),
                                                    kwargs = {'modelstate':modelstate,
                                                                'filter': filter}))

        else:
            modelstate = 'Error: Invalid form'
            viewmodel = SuperUser_Transfer.get_transfer_viewmodel(site_user, self.title, groupowner_id, filter, modelstate, form)
            return render(request, self.template_name, viewmodel)


class details(View):

    title = 'Group Owner - Details'
    template_name = 'app/shared_details_view.html'

    def get(self, request, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner_id = int(groupowner_id)
        filter = int(filter)

        viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, groupowner_id, filter, modelstate)

        return render(request, self.template_name, viewmodel)

class delete(View):

    title = 'Group Owner - Delete'
    template_name = 'app/shared_delete_view.html'

    def get(self, request, groupowner_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner_id = int(groupowner_id)
        filter = int(filter)

        viewmodel = SuperUser_Delete.get_delete_viewmodel(site_user, self.title, 
            groupowner_id, filter, modelstate)

        return render(request, self.template_name, viewmodel)

    def post(self, request, groupowner_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)
        
        modelstate = GroupOwner.delete_item(groupowner)

        return HttpResponseRedirect(reverse('groupowner:index', args=(),
                                    kwargs = {'modelstate':modelstate,
                                                'filter': filter}))
