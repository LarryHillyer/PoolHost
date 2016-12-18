from datetime import datetime

from django.db import models

from app.models import SiteUser, NFL_Division, NFL_Conference, League, Sport, SuperUser 
from app.models import NFL_Conference_Choices
from app.mixins import HelperMixins

from nfl.division.forms import NFL_DivisionForm_Create, NFL_DivisionForm_Edit

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, conferences, filter, 
        conference_id):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'division-id'

        self.viewmodel['conference_id'] = conference_id
        self.viewmodel['filter' ] = filter

        self.viewmodel['index_url'] = 'nfl:division:index'

        self.viewmodel['pagination_routing_html'] = 'nfl/nfl_pagination_routing.html'  
 
        self.viewmodel['conference_pagination_list_html'] = 'division/conference_pagination_list.html'

        self.viewmodel['shared_conference_pagination_list_html'] = 'nfl/shared_conference_pagination_list.html'
        self.viewmodel['shared_division_pagination_list_html'] = 'nfl/shared_division_pagination_list.html'

        self.viewmodel['conference_pagination_link_html'] = 'division/conference_pagination_link.html'
        self.viewmodel['division_pagination_link_html'] = 'division/division_pagination_link.html'
 

        self.viewmodel['conferences'] = conferences

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'nfl:division:create'
        self.viewmodel['create_link_name'] = 'Create Division'
        self.viewmodel['create_link_html'] =  'division/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'division/index_table.html'
        self.viewmodel['home_url'] = 'nfl:home'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        conference_id):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'division-id' 

        self.viewmodel['conference_id'] = conference_id
        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form 

        self.viewmodel['form_label_name'] = 'Division'
        self.viewmodel['form_label_conference'] = 'Conference'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['index_url'] = 'nfl:division:index'
        self.viewmodel['index_link_html'] = 'division/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'division-id' 

        self.viewmodel['division_id'] = division.id
        self.viewmodel['conference_id'] = conference_id
        self.viewmodel['filter'] = filter

        self.viewmodel['descriptive_list'] = 'division/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'nfl:division:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, divisions, conferences,  
        filter, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, conferences, filter,
            conference_id)
      
        self.viewmodel['items'] = divisions
        self.viewmodel['header_label_item'] = 'Division'
        self.viewmodel['header_label_conference'] = 'Conference'

        self.viewmodel['item_url'] = 'nfl:division:index'
        self.viewmodel['edit_url'] = 'nfl:division:edit' 
        self.viewmodel['details_url'] = 'nfl:division:details' 
        self.viewmodel['delete_url'] = 'nfl:division:delete' 

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id)

        self.viewmodel['item'] = division 
        self.viewmodel['item_label_name'] = 'Conference'
        self.viewmodel['item_label_league_name'] = 'League'
        self.viewmodel['item_label_sport_name'] = 'Sport'


class Create_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            conference_id)
        
        self.viewmodel['form_template_html'] = 'division/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'
        self.viewmodel['form_html'] = 'division/division_form.html'
        self.viewmodel['form_url'] = 'nfl:division:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        division_id, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            conference_id)
        
        self.viewmodel['division_id'] = division_id

        self.viewmodel['form_template_html'] = 'division/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_html'] = 'division/division_form.html'
        self.viewmodel['form_url'] = 'nfl:division:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id)

        self.viewmodel['details_links_html'] = 'division/details_links.html'
        self.viewmodel['edit_url'] = 'nfl:division:edit'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id)

        self.viewmodel['delete_form'] = 'division/delete_form.html'
        self.viewmodel['delete_url'] = 'nfl:division:delete'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, divisions, conferences,
        filter, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, divisions, conferences, 
            filter, conference_id) 

        self.viewmodel['use_pagination'] = True          
        
    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, conference_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        conference_id, divisions = SuperUser_Index.get_viewmodel_parameters_by_state(filter, conference_id)

        conferences = NFL_Conference.get_all_items(NFL_Conference)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, 
            divisions, conferences, filter, conference_id).viewmodel
        
        return viewmodel

    @classmethod
    def get_viewmodel_parameters_by_state(cls, filter, conference_id):

        if filter == 0:
            conference_id = 0
            divisions = NFL_Division.get_all_items(NFL_Division)

        elif filter == 1:

            conferences = NFL_Conference.get_all_items(NFL_Conference)

            if conferences.count() == 0:
                divisions = []               
                return conference_id, divisions

            if conference_id == 0:
                conference_id = NFL_Conference.get_conference_id_if_needed_and_possible(conferences, conference_id)       
               
            divisions = NFL_Division.get_items_by_conference_id(NFL_Division, conference_id)

        return conference_id, divisions

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            conference_id)
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, conference_id, form):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)
        
        conferences = NFL_Conference.get_all_items(NFL_Conference)
        NFL_Conference_Choices.get_choices_by_conferences(conferences)

        if form == None:
            form = NFL_DivisionForm_Create(initial={'conference_id': conference_id,
                                                            'filter' : filter})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            conference_id).viewmodel
        
        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        division_id, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            division_id, conference_id)

    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, filter, division_id, conference_id, 
        form):

        modelstate, modelsuccess_bool = NFL_Division.get_modelstate(modelstate)

        division = NFL_Division.get_item_by_id(NFL_Division, division_id)
        
        if form == None:       
            form = NFL_DivisionForm_Edit(initial = {'id': division.id,
                                                 'name': division.name,
                                                 'conference_id': division.conference_id,
                                                 'filter':filter})

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            division_id, conference_id).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, division_id, 
        conference_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        division = NFL_Division.get_item_by_id(NFL_Division, division_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id).viewmodel
        
        return viewmodel

class User_Delete(Delete_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, filter,
        division_id, conference_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        division = NFL_Division.get_item_by_id(NFL_Division, division_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelsuccess_bool, 
            division, filter, conference_id).viewmodel
        
        return viewmodel
