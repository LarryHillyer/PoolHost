from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from superuser.forms import SuperUserForm
from app.models import SuperUser, SiteUser

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
        
        superusers = SuperUser.get_all_items(SuperUser)
        view_model = SuperUser.get_index_view_model(site_user, modelstate, superusers)
        
        return render(request, self.template_name, view_model)
        
class create(View):

    form_class = SuperUserForm
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

        view_model = SuperUser.get_create_view_model(site_user, form, modelstate)

        return render(request, self.template_name, view_model)
    
    def post(self, request, modelstate = None, **kwargs):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        superuser = SuperUser(name = request.POST['name'])
        form = self.form_class(request.POST)
        if form.is_valid():

            same_superuser = SuperUser.objects.filter(name = superuser.name)
            if same_superuser.count() > 0:
                modelstate = 'Error: Superuser, ' + superuser.name + ' is already a superuser!'
                view_model = SuperUser.get_create_view_model(site_user, form, modelstate)
                return render(request, self.template_name, view_model)
                                
            site_user = SiteUser.get_item_by_name(SiteUser, superuser.name)          
            if site_user != None:

                site_user = SiteUser.make_siteuser_superuser(site_user) 
                superuser.user_id = site_user.user.id
                modelstate = SuperUser.add_item(SuperUser, superuser)

                return HttpResponseRedirect(reverse('superuser:superuser_index', args=(),
                                                    kwargs = {'modelstate':modelstate}))
            else:
                modelstate = 'Error: Superuser, ' + superuser.name + ' is not in database!'
                view_model = SuperUser.get_create_view_model(site_user, form, modelstate)
                return render(request, self.template_name, view_model)
        else:
            view_model = SuperUser.get_create_view_model(site_user, form, modelstate)
            return render(request, self.template_name, view_model)

class details(View):

    title = 'Super User - Details'
    template_name = 'app/shared_details.html'

    def get(self, request, superuser_id = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if superuser_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)
        view_model = SuperUser.get_details_and_delete_view_model(site_user, self.title, superuser)

        return render(request, self.template_name, view_model)

class delete(View):

    title = 'Super User - Delete'
    template_name = 'app/shared_delete.html'

    def get(self, request, superuser_id = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if superuser_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        view_model = SuperUser.get_details_and_delete_view_model(site_user, self.title, superuser)

        return render(request, self.template_name, view_model)

    def post(self, request, superuser_id = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if superuser_id == None:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        modelstate = SuperUser.delete_item(superuser)

        return HttpResponseRedirect(reverse('superuser:superuser_index', args=(),
                                    kwargs = {'modelstate':modelstate}))
