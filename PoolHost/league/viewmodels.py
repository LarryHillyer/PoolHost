from datetime import datetime

from django.db import models

from app.models import SiteUser, League, Sport, SuperUser, Sport_Choices
from app.mixins import HelperMixins

from league.forms import LeagueForm_Create, LeagueForm_Edit

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, sports, 
        filter, sport_id):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'league-id'

        self.viewmodel['sport_id'] = sport_id
        self.viewmodel['filter' ] = filter

        self.viewmodel['index_url'] = 'league:index'

        self.viewmodel['pagination_routing_html'] = 'app/sports_pagination_routing.html'  
 
        self.viewmodel['sport_pagination_list_html'] = 'league/sport_pagination_list.html'

        self.viewmodel['shared_sport_pagination_list_html'] = 'app/shared_sport_pagination_list.html'

        self.viewmodel['sport_pagination_link_html'] = 'league/sport_pagination_link.html'
                   
        self.viewmodel['sports'] = sports

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'league:create'
        self.viewmodel['create_link_name'] = 'Create League'
        self.viewmodel['create_link_html'] =  'league/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'league/index_table.html' 

        self.viewmodel['home_url'] = 'home'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        sport_id):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'league-id' 

        self.viewmodel['sport_id'] = sport_id
        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'league/league_form.html'

        self.viewmodel['form_label_name'] = 'League'
        self.viewmodel['form_label_sport'] = 'Sport'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'league:index'
        self.viewmodel['index_link_html'] = 'league/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            league, filter, sport_id):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'league-id' 

        self.viewmodel['league_id'] = league.id
        self.viewmodel['sport_id'] = sport_id
        self.viewmodel['filter'] = filter

        self.viewmodel['descriptive_list'] = 'league/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'league:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, leagues,   
        sports, filter, sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, sports, 
            filter, sport_id)
      
        self.viewmodel['items'] = leagues 
        self.viewmodel['header_label_item'] = 'League'
        self.viewmodel['header_label_sport'] = 'Sport' 
        self.viewmodel['item_url'] = 'league:redirect'
        self.viewmodel['transfer_url'] = 'league:transfer' 
        self.viewmodel['edit_url'] = 'league:edit'
        self.viewmodel['details_url'] = 'league:details' 
        self.viewmodel['delete_url'] = 'league:delete' 

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            league, filter, sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            league, filter, sport_id)

        self.viewmodel['item'] = league 
        self.viewmodel['item_label_name'] = 'League'
        self.viewmodel['item_label_sport_name'] = 'Sport'

                       
class Create_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            sport_id)
        
        self.viewmodel['form_template_html'] = 'league/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'
        self.viewmodel['form_url'] = 'league:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        league_id, sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            sport_id)
        
        self.viewmodel['league_id'] = league_id

        self.viewmodel['form_template_html'] = 'league/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_url'] = 'league:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, league,  
        filter, sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, league,  
        filter, sport_id)

        self.viewmodel['edit_url'] = 'league:edit'
        self.viewmodel['transfer_url'] = 'league:transfer'
        self.viewmodel['details_links_html'] = 'league/details_links.html'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, league,  
        filter, sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, league,  
        filter, sport_id)

        self.viewmodel['delete_url'] = 'league:delete'
        self.viewmodel['delete_form'] = 'league/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, leagues, sports, filter,
        sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, leagues, sports, filter, 
            sport_id) 

        self.viewmodel['use_pagination'] = True            

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, sport_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        sport_id, leagues = SuperUser_Index.get_viewmodel_parameters_by_state(filter, sport_id)
        
        sports = Sport.get_all_items(Sport) 

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, leagues, sports, filter, sport_id).viewmodel
        
        return viewmodel

    @classmethod
    def get_viewmodel_parameters_by_state(cls, filter, sport_id):

        if filter == 0:
            sport_id = 0
            leagues = League.get_all_items(League)

        elif filter == 1:

            sports = Sport.get_all_items(Sport)

            if sports.count() == 0:
                leagues = []               
                return sport_id, leagues

            if sport_id == 0:
                sport_id = Sport.get_sport_id_if_needed_and_possible(sports, sport_id)       
               
            leagues = League.get_items_by_sport_id(League, sport_id)

        return sport_id, leagues

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            sport_id)
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, sport_id, form):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)
        sports = Sport.get_all_items(Sport)
        if sports.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        sport_id = Sport.get_sport_id_if_needed_and_possible(sports, sport_id)
        Sport_Choices.get_choices_by_sports(sports)

        if form == None:
            form = LeagueForm_Create(initial={'sport_id' : sport_id,
                                                        'filter' : filter})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            sport_id).viewmodel
        
        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        league_id, sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            league_id, sport_id)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, filter, league_id, sport_id, form):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        league = League.get_item_by_id(League, league_id)

        sport_id = league.sport_id
        sports = Sport.get_all_items(Sport)
        Sport_Choices.get_choices_by_sports(sports)
        
        if form == None:       
            form = LeagueForm_Edit(initial = {'id': league.id,
                                                 'name': league.name,
                                                 'sport_id': league.sport_id,
                                                 'filter':filter})

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            league_id, sport_id).viewmodel
        
        return viewmodel


class SuperUser_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, league, 
        filter, sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, league, 
            filter, sport_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, league_id, 
        sport_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)
        league = League.get_item_by_id(League, league_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, 
            league, filter, sport_id).viewmodel
        
        return viewmodel


class User_Delete(Delete_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, league, filter,
        sport_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, league, filter,
            sport_id) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, filter, league_id,
        sport_id):

        modelstate, modelsuccess_bool = League.get_modelstate(modelstate)

        league = League.get_item_by_id(League, league_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelsuccess_bool, league, 
            filter, sport_id).viewmodel
        
        return viewmodel
