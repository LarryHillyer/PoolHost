from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import NFL_Division, NFL_Conference, League, Sport, SiteUser

from nfl.division.viewmodels import SuperUser_Index,  SuperUser_Create, SuperUser_Edit, SuperUser_Details
from nfl.division.viewmodels import User_Delete

from nfl.division.forms import NFL_DivisionForm_Create, NFL_DivisionForm_Edit

class index(View):

    title = 'NFL Divisions - Index'
    template_name = 'app/shared_index_view.html'

    def get(self, request, filter = 0, conference_id = 0, modelstate = None ):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(conference_id)
        filter = int(filter)

        viewmodel = SuperUser_Index.get_index_viewmodel(site_user, self.title, 
            modelstate, filter, conference_id)
        
        return render(request, self.template_name, viewmodel)

class create(View):

    title = 'NFL Division - Create'
    template_name = 'app/shared_form_view.html'

    def get(self, request, conference_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(conference_id)
        filter = int(filter)
        form = None

        viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
            modelstate, filter, conference_id, form)

        if viewmodel['modelstate'] != None and viewmodel['modelstate'] != "":
            if viewmodel['modelstate'].split(':')[0] != 'Success':
                return HttpResponseRedirect(reverse('division:index', args = (),
                                                kwargs = {'modelstate': viewmodel['modelstate'],
                                                            'conference_id': conference_id,
                                                            'filter' : filter}))

        return render(request, self.template_name, viewmodel)

    def post(self, request, conference_id = 0, filter = 0, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        conference_id = int(request.POST['conference_id'])
        filter = int(request.POST['filter'])

        form = NFL_DivisionForm_Create(request.POST)
        
        if form.is_valid():


            divisions = NFL_Division.get_items_by_conference_id(NFL_Division, int(form.data['conference_id']))

            divisions = divisions.filter(name = form.data['name'])

            if divisions.count() == 0:

                division = NFL_Division(name = form.data['name'], conference_id = int(form.data['conference_id']))

                modelstate = NFL_Division.add_item(NFL_Division, division)

                return HttpResponseRedirect(reverse('nfl:division:index', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'conference_id': conference_id,
                                                                'filter' : filter}))
            else:

                modelstate = 'Error: Division, ' + form.data['name'] + ' is already a NFL_Division!!!'

                viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                    modelstate, filter, conference_id, form)

                return render(request, self.template_name, viewmodel)


        else:
            modelstate = 'Error: Invalid Data!!! '

            viewmodel = SuperUser_Create.get_create_viewmodel(site_user, self.title, 
                modelstate, filter, conference_id, form)

            return render(request, self.template_name, viewmodel)
      
class edit(View):
    title = 'NFL Division - Edit'
    template_name = 'app/shared_form_view.html'

    def get(self, request, division_id = 0, conference_id = 0, 
        filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        division_id = int(division_id)
        conference_id = int(conference_id)
        filter = int(filter)
        form = None

        viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, filter, 
            division_id, conference_id, form)

        return render(request, self.template_name, viewmodel)

    def post(self, request, division_id = 0, conference_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        division_id = int(request.POST['id'])
        conference_id = int(request.POST['conference_id'])
        filter = int(request.POST['filter'])

        form = NFL_DivisionForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_division = NFL_Division.get_exactly_same_division(int(form.data['id']), 
                form.data['name'], conference_id)

            if exactly_same_division.count() > 0:

                modelstate = 'Error: No Changes were made to NFL Division, ' + form.data['name'] + ' update aborted!'

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, filter, division_id, conference_id, form)

                return render(request, self.template_name, viewmodel)
   
            same_division = NFL_Division.get_same_division_in_database(form.data['name'], conference_id) 

            if same_division.count() > 0:
                modelstate = 'Error: NFL Division, ' + form.data['name'] + ' is already in the database, update aborted!'    

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, filter, division_id, conference_id, form)

                return render(request, self.template_name, viewmodel)

            division = NFL_Division.get_item_by_id(NFL_Division, int(form.data['id']))
            division.name = form.data['name']
            division.conference_id = conference_id
            modelstate = NFL_Division.edit_item(NFL_Division, division)

            if modelstate.split(':')[0] != 'Success':

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                    modelstate, filter, division_id, conference_id, form)

                return render(request, self.template_name, viewmodel)

            return HttpResponseRedirect(reverse('nfl:division:index', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'conference_id': conference_id,
                                                            'filter' : form.data['filter']}))

        else:
            modelstate = 'Error: Invalid Input!'

            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, 
                modelstate, filter, division_id, conference_id, form)

            return render(request, self.template_name, viewmodel)

class details(View):
    title = 'NFL Division - Details'
    template_name = 'app/shared_details_view.html'

    def get(self,request, division_id = 0, conference_id = 0, filter = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        division_id = int(division_id)
        conference_id = int(conference_id)
        filter = int(filter)

        if division_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        viewmodel = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
            modelstate, filter, division_id, conference_id)
        
        return render(request, self.template_name, viewmodel)

class delete(View):
    title = 'NFL Division - Delete'
    template_name = 'app/shared_delete_view.html'

    def get(self,request, division_id = 0, conference_id = 0, filter = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if division_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        division_id = int(division_id)
        conference_id = int(conference_id)
        filter = int(filter)

        viewmodel = User_Delete.get_delete_viewmodel(site_user, self.title, 
               modelstate, filter, division_id, conference_id)
        
        return render(request, self.template_name, viewmodel)

    def post(self, request, division_id = 0, conference_id = 0, filter = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if not site_user.is_superuser:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if division_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        division_id = int(division_id)
        conference_id = int(conference_id)
        filter = int(filter)

        division = NFL_Division.get_item_by_id(NFL_Division, division_id)
        modelstate = NFL_Division.delete_item(division)

        return HttpResponseRedirect(reverse('nfl:division:index', args=(),
                                    kwargs = {'modelstate': modelstate,
                                                'conference_id': conference_id,
                                                'filter': filter}))
