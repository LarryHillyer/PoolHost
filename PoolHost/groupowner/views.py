from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from groupowner.forms import GroupOwnerForm
from app.models import GroupOwner, SiteUser


class index(View):

    template_name = 'app/shared_index.html'
    def get(self, request, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowners = GroupOwner.get_all_items(GroupOwner)
        view_model = GroupOwner.get_index_view_model(site_user, modelstate, groupowners)
        
        return render(request, self.template_name, view_model)


class create(View):

    form_class = GroupOwnerForm
    template_name = 'app/shared_create.html'

    def get(self, request, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        form = self.form_class()

        view_model = GroupOwner.get_create_view_model(site_user, form, modelstate)

        return render(request, self.template_name, view_model)
    
    def post(self, request, modelstate = None, **kwargs):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner = GroupOwner(name = request.POST['name'])
        form = self.form_class(request.POST)
        if form.is_valid():

            same_groupowner = GroupOwner.get_items_by_name(GroupOwner, groupowner.name)
            if same_groupowner.count() > 0:
                modelstate = 'Error: groupowner, ' + groupowner.name + ' is already a groupowner!'
                view_model = GroupOwner.get_create_view_model(site_user, form, modelstate)
                return render(request, self.template_name, view_model)
                                
            site_user = SiteUser.get_item_by_name(SiteUser, groupowner.name)          
            if site_user != None:

                site_user = SiteUser.make_siteuser_groupowner(site_user) 
                groupowner.user_id = site_user.user.id
                modelstate = GroupOwner.add_item(GroupOwner, groupowner)

                return HttpResponseRedirect(reverse('groupowner:groupowner_index', args=(),
                                                    kwargs = {'modelstate':modelstate}))
            else:
                modelstate = 'Error: groupowner, ' + groupowner.name + ' is not in database!'
                view_model = GroupOwner.get_create_view_model(site_user, form, modelstate)
                return render(request, self.template_name, view_model)
        else:
            view_model = GroupOwner.get_create_view_model(site_user, form, modelstate)
            return render(request, self.template_name, view_model)

class details(View):

    title = 'Group Owner - Delete'
    template_name = 'app/shared_details.html'

    def get(self, request, groupowner_id = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)

        view_model = GroupOwner.get_details_and_delete_view_model(site_user, self.title, groupowner)

        return render(request, self.template_name, view_model)

class delete(View):

    title = 'Group Owner - Delete'
    template_name = 'app/shared_delete.html'

    def get(self, request, groupowner_id = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)

        view_model = GroupOwner.get_details_and_delete_view_model(site_user, self.title, groupowner)

        return render(request, self.template_name, view_model)

    def post(self, request, groupowner_id = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if groupowner_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)

        modelstate = GroupOwner.delete_item(groupowner)

        return HttpResponseRedirect(reverse('groupowner:groupowner_index', args=(),
                                    kwargs = {'modelstate':modelstate}))
