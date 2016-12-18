from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import NFL_Conference, League, Sport, SiteUser

from nfl.conference.viewmodels import SuperUser_Index,  SuperUser_Create, SuperUser_Edit, SuperUser_Details
from nfl.conference.viewmodels import User_Delete

from nfl.conference.forms import NFL_ConferenceForm_Create, NFL_ConferenceForm_Edit

class index(View):

    title = 'NFL Conferences - Index'
    template_name = 'app/shared_index_view.html'

    def get(self, request, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, 
            modelstate)
        
        return render(request, self.template_name, viewmodel)

class create(View):

    title = 'NFL Conference - Create'
    template_name = 'app/shared_form_view.html'

    def get(self, request, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        form = None

        viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate, form)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('conference:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],}))

        return render(request, self.template_name, viewmodel)

    def post(self, request, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        form = NFL_ConferenceForm_Create(request.POST)
        
        if form.is_valid():

            league_id = League.get_item_by_name(League, 'NFL').id
            
            conferences = NFL_Conference.get_items_by_league_id(NFL_Conference, 
                league_id)

            conferences = conferences.filter(name = form.data['name'])

            if conferences.count() == 0:

                conference = NFL_Conference(name = form.data['name'], 
                    league_id = league_id)

                modelstate = NFL_Conference.add_item(NFL_Conference, conference)

                return HttpResponseRedirect(reverse('nfl:conference:index', args = (),
                                                    kwargs = {'modelstate': modelstate,}))
            else:

                modelstate = 'Error: Conference, ' + form.data['name'] + ' is already a NFL_Conference!!!'

                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                    modelstate, form)

                return render(request, self.template_name, viewmodel)

        else:
            modelstate = 'Error: Invalid Data!!! '

            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate, form)

            return render(request, self.template_name, viewmodel)
      
class edit(View):
    title = 'NFL Conference - Edit'
    template_name = 'app/shared_form_view.html'

    def get(self, request, conference_id = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(conference_id)
        form = None

        viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
            conference_id, form)

        return render(request, self.template_name, viewmodel)

    def post(self, request, conference_id = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(request.POST['id'])
        form = NFL_ConferenceForm_Edit(request.POST)

        if form.is_valid():

            league_id = League.get_item_by_name(League, 'NFL').id

            exactly_same_conference = NFL_Conference.get_exactly_same_conference(int(form.data['id']), 
                form.data['name'], league_id)

            if exactly_same_conference.count() > 0:

                modelstate = 'Error: No Changes were made to NFL Conference, ' + form.data['name'] + ' update aborted!'

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate,conference_id, form)

                return render(request, self.template_name, viewmodel)
   
            same_conference = NFL_Conference.get_same_conference_in_database(form.data['name'], league_id) 

            if same_conference.count() > 0:
                modelstate = 'Error: NFL Conference, ' + form.data['name'] + ' is already in the database, update aborted!'    

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, conference_id, form)

                return render(request, self.template_name, viewmodel)

            conference = NFL_Conference.get_item_by_id(NFL_Conference, int(form.data['id']))
            conference.name = form.data['name']
            conference.league_id = league_id
            modelstate = NFL_Conference.edit_item(NFL_Conference, conference)

            if modelstate.split(':')[0] != 'Success':

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, conference_id, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('nfl:conference:index', args = (),
                                                kwargs = {'modelstate': modelstate}))

        else:
            modelstate = 'Error: Invalid Input!'

            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                modelstate, conference_id, form)

            return render(request, self.template_name, viewmodel)

class details(View):
    title = 'NFL Conference - Details'
    template_name = 'app/shared_details_view.html'

    def get(self,request, conference_id = 0, league_id = 0, sport_id = 0, 
        filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(conference_id)

        if conference_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
            modelstate, conference_id)
        
        return render(request, self.template_name, viewmodel)

class delete(View):
    title = 'NFL Conference - Delete'
    template_name = 'app/shared_delete_view.html'

    def get(self,request, conference_id = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if conference_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(conference_id)

        viewmodel = User_Delete.get_delete_viewmodel(site_user, self.title, 
               modelstate, conference_id)
        
        return render(request, self.template_name, viewmodel)

    def post(self, request, conference_id = 0, league_id = 0, filter = 0, sport_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if conference_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(conference_id)

        conference = NFL_Conference.get_item_by_id(NFL_Conference, conference_id)
        modelstate = NFL_Conference.delete_item(conference)

        return HttpResponseRedirect(reverse('nfl:conference:index', args=(),
                                    kwargs = {'modelstate': modelstate}))
