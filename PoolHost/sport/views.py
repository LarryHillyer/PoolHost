from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import Sport, SiteUser

from sport.viewmodels import SuperUser_Index, SuperUser_Create, SuperUser_Edit, SuperUser_Details, SuperUser_Delete
from sport.forms import SportForm_Create, SportForm_Edit

class index(View):

    template_name = 'app/shared_index_view.html'
    title = 'Sport - Index'
    
    def get(self, request, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')
        
        view_model = SuperUser_Index.get_index_viewmodel(site_user,self.title, modelstate, filter)
        
        return render(request, self.template_name, view_model)
        
class create(View):

    template_name = 'app/shared_form_view.html'
    title = 'Sport - Create'

    def get(self, request, filter = 0, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        filter = int(filter)
        form = None

        view_model = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate, filter, form)

        return render(request, self.template_name, view_model)
    
    def post(self, request, filter = 0, modelstate = None, **kwargs):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        filter = int(filter)
        form = SportForm_Create(request.POST)

        if form.is_valid():

            sport = Sport(name = request.POST['name'])

            same_sport = Sport.objects.filter(name = sport.name)
            if same_sport.count() > 0:
                modelstate = 'Error: Sport, ' + sport.name + ' is already a sport!'

                view_model = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate, 
                    filter, form)

                return render(request, self.template_name, view_model)
                                
            modelstate = Sport.add_item(Sport, sport)

            return HttpResponseRedirect(reverse('sport:index', args=(),
                                            kwargs = {'modelstate':modelstate,
                                                        'filter': filter}))
        else:
            modelstate = 'Error: Invalid Input!'

            view_model = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate, 
                filter, form)

            return render(request, self.template_name, view_model)

class edit(View):
    title = 'Sport - Edit'
    template_name = 'app/shared_form_view.html'

    def get(self, request, sport_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if sport_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')
            
        sport_id = int(sport_id)
        filter = int(filter)
        form = None

        viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, sport_id, filter, form)

        return render(request, self.template_name, viewmodel)

    def post(self, request, sport_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        sport_id = int(sport_id)
        filter = int(filter)

        form = SportForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_sport = Sport.get_exactly_same_sport(form.data['id'], 
                form.data['name'])

            if exactly_same_sport.count() > 0:

                modelstate = 'Error: No Changes were made during edit, update aborted!'

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title,
                        modelstate, sport_id, filter, form)

                return render(request, self.template_name, viewmodel)
   
            same_sport = Sport.get_same_sport_in_database(form.data['name']) 

            if same_sport.count() > 0:
                modelstate = 'Error: Sport is already in the database, update aborted!'    

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                    sport_id, filter, form)

                return render(request, self.template_name, viewmodel)

            sport = Sport.get_item_by_id(Sport, form.data['id'])
            sport.name = form.data['name']
            modelstate = Sport.edit_item(Sport, sport)

            if modelstate.split(':')[0] != 'Success':

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                    sport_id, filter, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('sport:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'filter': filter}))

        else:
            modelstate = 'Error: Invalid Input!'
 
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                sport_id, filter, form)

            return render(request, self.template_name, viewmodel)

class details(View):

    title = 'Sport - Details'
    template_name = 'app/shared_details_view.html'

    def get(self, request, sport_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if sport_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        sport_id = int(sport_id)
        view_model = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
            modelstate, sport_id, filter )

        return render(request, self.template_name, view_model)

class delete(View):

    title = 'Sport - Delete'
    template_name = 'app/shared_delete_view.html'

    def get(self, request, sport_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if sport_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        sport_id = int(sport_id)

        view_model = SuperUser_Delete.get_delete_viewmodel(site_user, self.title, 
            modelstate, sport_id, filter )

        return render(request, self.template_name, view_model)

    def post(self, request, sport_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if sport_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        sport_id = int(sport_id)
        sport = Sport.get_item_by_id(Sport, sport_id)

        modelstate = Sport.delete_item(Sport, sport)

        return HttpResponseRedirect(reverse('sport:index', args=(),
                                    kwargs = {'modelstate':modelstate,
                                                'filter': filter}))
