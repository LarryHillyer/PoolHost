from datetime import datetime

from django.db import models

from app.models import SiteUser, NFL_Conference, League, Sport, SuperUser 
from app.models import Sport_Choices, League_Choices, NFL_Conference_Choices
from app.mixins import HelperMixins

from nfl.conference.forms import NFL_ConferenceForm_Create, NFL_ConferenceForm_Edit

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'conference-id'

        self.viewmodel['index_url'] = 'nfl:conference:index'

        self.viewmodel['pagination_routing_html'] = 'app/sports_pagination_routing.html'  
 
        self.viewmodel['sport_pagination_list_html'] = 'conference/sport_pagination_list.html'

        self.viewmodel['shared_sport_pagination_list_html'] = 'app/shared_sport_pagination_list.html'
        self.viewmodel['shared_league_pagination_list_html'] = 'app/shared_league_pagination_list.html'
        self.viewmodel['shared_conference_pagination_list_html'] = 'app/shared_conference_pagination_list.html'
        self.viewmodel['shared_division_pagination_list_html'] = 'app/shared_division_pagination_list.html'

        self.viewmodel['sport_pagination_link_html'] = 'conference/sport_pagination_link.html'
        self.viewmodel['league_pagination_link_html'] = 'conference/league_pagination_link.html'
        
        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'nfl:conference:create'
        self.viewmodel['create_link_name'] = 'Create Conference'
        self.viewmodel['create_link_html'] =  'conference/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'conference/index_table.html'

        self.viewmodel['home_url'] = 'nfl:home'


        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'conference-id' 

        self.viewmodel['form'] = form 

        self.viewmodel['form_label_name'] = 'Conference'
        self.viewmodel['form_label_sport'] = 'Sport'
        self.viewmodel['form_label_league'] = 'League'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['index_url'] = 'nfl:conference:index'
        self.viewmodel['index_link_html'] = 'conference/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            conference):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'conference-id' 

        self.viewmodel['conference_id'] = conference.id

        self.viewmodel['descriptive_list'] = 'conference/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'nfl:conference:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, conferences):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
      
        self.viewmodel['items'] = conferences
        self.viewmodel['header_label_item'] = 'Conference'
        self.viewmodel['header_label_league'] = 'League'
        self.viewmodel['header_label_sport'] = 'Sport'

        self.viewmodel['item_url'] = 'nfl:division:index'
        self.viewmodel['edit_url'] = 'nfl:conference:edit' 
        self.viewmodel['details_url'] = 'nfl:conference:details' 
        self.viewmodel['delete_url'] = 'nfl:conference:delete' 

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            conference):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            conference)

        self.viewmodel['item'] = conference 
        self.viewmodel['item_label_name'] = 'Conference'
        self.viewmodel['item_label_league_name'] = 'League'
        self.viewmodel['item_label_sport_name'] = 'Sport'


class Create_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)
        
        self.viewmodel['form_template_html'] = 'conference/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'
        self.viewmodel['form_html'] = 'conference/conference_form.html'
        self.viewmodel['form_url'] = 'nfl:conference:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        conference_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)
        
        self.viewmodel['conference_id'] = conference_id

        self.viewmodel['form_template_html'] = 'conference/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_html'] = 'conference/conference_form.html'
        self.viewmodel['form_url'] = 'nfl:conference:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            conference):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            conference)

        self.viewmodel['details_links_html'] = 'conference/details_links.html'
        self.viewmodel['edit_url'] = 'nfl:conference:edit'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            conference):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            conference)

        self.viewmodel['delete_form'] = 'conference/delete_form.html'
        self.viewmodel['delete_url'] = 'nfl:conference:delete'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, conferences):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, conferences) 

        self.viewmodel['use_pagination'] = False          
        
    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        conferences = NFL_Conference.get_all_items(NFL_Conference)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, 
            conferences).viewmodel
        
        return viewmodel

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, form):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        league_id = League.get_item_by_name(League, 'NFL').id

        if form == None:
            form = NFL_ConferenceForm_Create(initial={'league_id': league_id})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form).viewmodel
        
        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        conference_id,):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            conference_id,)

    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, conference_id, form):

        modelstate, modelsuccess_bool = NFL_Conference.get_modelstate(modelstate)

        conference = NFL_Conference.get_item_by_id(NFL_Conference, conference_id)
        
        if form == None:       
            form = NFL_ConferenceForm_Edit(initial = {'id': conference.id,
                                                 'name': conference.name,})

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            conference_id).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            conference):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            conference) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, conference_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        conference = NFL_Conference.get_item_by_id(NFL_Conference, conference_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, 
            conference).viewmodel
        
        return viewmodel


class User_Delete(Delete_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            conference):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            conference) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, conference_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        conference = NFL_Conference.get_item_by_id(NFL_Conference, conference_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelsuccess_bool, 
            conference).viewmodel
        
        return viewmodel
