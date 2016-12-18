from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import League, Sport, SiteUser

from league.viewmodels import SuperUser_Index,  SuperUser_Create, SuperUser_Edit, SuperUser_Details
from league.viewmodels import User_Delete

from league.forms import LeagueForm_Create, LeagueForm_Edit

class index(View):

    title = 'League - Index'
    template_name = 'app/shared_index_view.html'

    def get(self, request, filter = 0, sport_id = 0, modelstate = None ):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        sport_id = int(sport_id)
        filter = int(filter)

        viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, modelstate, filter, sport_id)
        
        return render(request, self.template_name, viewmodel)

class create(View):

    title = 'League - Create'
    template_name = 'app/shared_form_view.html'

    def get(self,request, sport_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        sport_id = int(sport_id)
        filter = int(filter)
        form = None

        viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
            modelstate, filter, sport_id, form)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('league:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],
                                                            'sport_id': sport_id,
                                                            'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request,  sport_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        sport_id = int(request.POST['sport_id'])
        filter = int(request.POST['filter'])

        form = LeagueForm_Create(request.POST)
            
        if form.is_valid():
            same_league = League.get_same_league_in_database(form.data['name'], sport_id)
            if same_league.count() > 0:
                modelstate = 'Error: Pool Group, ' + form.data['name'] + ' has already been taken!'

                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                    modelstate, filter, sport_id, form)

                return render(request, self.template_name, viewmodel)
            
            league = League(name = form.data['name'], sport_id = sport_id)
            modelstate = League.add_item(League, league)

            if modelstate.split(':')[0] != 'Success':

                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                    modelstate, filter, sport_id, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('league:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'sport_id': sport_id,
                                                            'filter' : form.data['filter']}))

        else:

            modelstate = 'Error: Invalid Input!'
 
            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate, filter,
                sport_id, form)

            return render(request, self.template_name, viewmodel)

class edit(View):
    title = 'League - Edit'
    template_name = 'app/shared_form_view.html'

    def get(self, request, league_id = 0, sport_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser and not site_user.is_sport:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        league_id = int(league_id)
        sport_id = int(sport_id)
        filter = int(filter)
        form = None

        viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, filter, league_id,  sport_id, form)

        return render(request, self.template_name, viewmodel)

    def post(self, request, league_id = 0, sport_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        league_id = int(request.POST['id'])
        sport_id = int(request.POST['sport_id'])
        filter = int(request.POST['filter'])

        form = LeagueForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_league = League.get_exactly_same_league(form.data['id'], 
                form.data['name'], sport_id)

            if exactly_same_league.count() > 0:

                modelstate = 'Error: No Changes were made to Pool Group, ' + form.data['name'] + ' update aborted!'

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, filter, league_id, sport_id, form)

                return render(request, self.template_name, viewmodel)
   
            same_league = League.get_same_league_in_database(form.data['name'], 
                sport_id) 

            if same_league.count() > 0:
                modelstate = 'Error: League, ' + form.data['name'] + ' is already in the database, update aborted!'    

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, filter,  league_id, sport_id, form)

                return render(request, self.template_name, viewmodel)

            league = League.get_item_by_id(League, form.data['id'])
            league.name = form.data['name']
            league.sport_id = sport_id
            modelstate = League.edit_item(League, league)

            if modelstate.split(':')[0] != 'Success':

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, filter, league_id, sport_id, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('league:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'sport_id': sport_id,
                                                            'filter' : form.data['filter']}))

        else:
            modelstate = 'Error: Invalid Input!'

            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                modelstate, filter, league_id, sport_id, form)

            return render(request, self.template_name, viewmodel)
 
  
class details(View):

    title = 'League - Details'
    template_name = 'app/shared_details_view.html'

    def get(self,request, league_id = 0, sport_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        league_id = int(league_id)
        sport_id = int(sport_id)
        filter = int(filter)

        if league_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, modelstate, filter, league_id,
            sport_id)
        
        return render(request, self.template_name, viewmodel)
        
class delete(View):

    title = 'League - Delete'
    template_name = 'app/shared_delete_view.html'

    def get(self,request, league_id = 0, sport_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if league_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        league_id = int(league_id)
        sport_id = int(sport_id)
        filter = int(filter)

        viewmodel = User_Delete.get_delete_viewmodel(site_user, self.title, 
               modelstate, filter, league_id, sport_id)
        
        return render(request, self.template_name, viewmodel)

    def post(self, request, league_id = 0, filter = 0, sport_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if league_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        league_id = int(league_id)
        sport_id = int(sport_id)
        filter = int(filter)

        league = League.get_item_by_id(League, league_id)
        modelstate = League.delete_item(league)

        return HttpResponseRedirect(reverse('league:index', args=(),
                                    kwargs = {'modelstate': modelstate,
                                                'sport_id': sport_id,
                                                'filter': filter}))

class league_redirect(View):

    def get (self, request, filter = 0, league_id = 0, sport_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        league_id = int(league_id)
        sport_id = int(sport_id)
        filter = int(filter)

        if league_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        league = League.get_item_by_id(League, league_id)

        if league.name == 'NFL':
            return HttpResponseRedirect(reverse('nfl:conference:index'))

        
