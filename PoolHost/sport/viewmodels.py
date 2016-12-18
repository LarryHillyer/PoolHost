from datetime import datetime

from django.db import models

from app.models import SiteUser, Sport
from app.mixins import HelperMixins

from sport.forms import SportForm_Create, SportForm_Edit

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, filter):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'sport-id'

        self.viewmodel['filter'] = filter

        self.viewmodel['index_url'] = 'sport:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'sport:create'
        self.viewmodel['create_link_name'] = 'Create Sport'
        self.viewmodel['create_link_html'] =  'sport/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'sport/index_table.html' 

        self.viewmodel['home_url'] = 'home'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'sport-id'

        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'sport/sport_form.html'

        self.viewmodel['form_label_name'] = 'Cron Job'
        self.viewmodel['form_label_sporttype'] = 'Cron Job Type'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'sport:index'
        self.viewmodel['index_link_html'] = 'sport/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            sport, filter):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'sport-id' 

        self.viewmodel['sport_id'] = sport.id
        self.viewmodel['filter'] = filter

        self.viewmodel['descriptive_list'] = 'sport/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'sport:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, sports, filter):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, filter)
      
        self.viewmodel['items'] = sports 
        self.viewmodel['header_label_item'] = 'Sport'
        self.viewmodel['item_url'] = 'league:index'
        self.viewmodel['edit_url'] = 'sport:edit' 
        self.viewmodel['details_url'] = 'sport:details' 
        self.viewmodel['delete_url'] = 'sport:delete'

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            sport, filter):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            sport, filter)

        self.viewmodel['item'] = sport 
        self.viewmodel['item_label_name'] = 'Sport'


class Create_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter)

        self.viewmodel['form_template_html'] = 'sport/create_form.html' 
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html' 
        self.viewmodel['form_url'] = 'sport:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        sport_id, filter):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter)
        
        self.viewmodel['sport_id'] = sport_id

        self.viewmodel['form_template_html'] = 'sport/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_url'] = 'sport:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, sport, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, sport, filter)

        self.viewmodel['edit_url'] = 'sport:edit'
        self.viewmodel['details_links_html'] = 'sport/details_links.html'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, sport, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, sport, filter)

        self.viewmodel['delete_url'] = 'sport:delete'
        self.viewmodel['delete_form'] = 'sport/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, sports, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, sports, filter)

        self.viewmodel['use_pagination'] = False            
        
    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter):

        modelstate, modelsuccess_bool = Sport.get_modelstate(modelstate)
        sports = Sport.get_all_items(Sport)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, 
            sports, filter).viewmodel

        return viewmodel

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form, filter)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, form):

        modelstate, modelsuccess_bool = Sport.get_modelstate(modelstate)

        if form == None:
            form = SportForm_Create(initial = {})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, 
            form, filter).viewmodel

        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        sport_id, filter):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            sport_id, filter)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, sport_id, filter, form):

        modelstate, modelsuccess_bool = Sport.get_modelstate(modelstate)

        sport = Sport.get_item_by_id(Sport, sport_id)

        if form == None:
            form = SportForm_Edit(instance = sport, initial = {})

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            sport_id, filter).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, sport, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, sport, filter)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, sport_id, filter):

        modelstate, modelsuccess_bool = Sport.get_modelstate(modelstate)

        sport = Sport.get_item_by_id(Sport, sport_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, sport, filter).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, sport, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, sport, filter)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, sport_id, filter):

        modelstate, modelsuccess_bool = Sport.get_modelstate(modelstate)

        sport = Sport.get_item_by_id(Sport, sport_id)

        viewmodel = SuperUser_Delete(site_user, title, modelstate, modelsuccess_bool, sport, filter).viewmodel

        return viewmodel
