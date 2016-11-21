from datetime import datetime

from django.db import models

from app.models import SiteUser, SuperUser
from app.mixins import HelperMixins

class BaseViewModel(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, superusers):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'superuser-id' # app/shared_index.html params
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate'] =  modelstate
        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']
        self.viewmodel['create_url'] = 'superuser:create'
        self.viewmodel['create_name'] = 'Create Super User'
        self.viewmodel['index_table'] = 'superuser/index_table.html'

        self.viewmodel['items'] = superusers # super_user/index_table.html params
        self.viewmodel['header_label_item'] = 'Super User Name' 
        self.viewmodel['details_url'] = 'superuser:details' 
        self.viewmodel['delete_url'] = 'superuser:delete'
 

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelstate_bool = SuperUser.get_modelstate(modelstate)
        superusers = SuperUser.get_all_items(SuperUser)

        viewmodel = Index_ViewModel(site_user, title, modelstate, modelstate_bool, superusers).viewmodel

        return viewmodel

class Create_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, form, modelstate, modelstate_bool):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'superuser-id' # shared_create params
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['create_url'] = 'superuser:create'
        self.viewmodel['create_form'] = 'superuser/superuser_form.html'
        self.viewmodel['index_url'] = 'superuser:index'
        self.viewmodel['scripts'] = ['app/scripts/jqueryvalidate.js']

        self.viewmodel['form'] = form # superuser_form params
        self.viewmodel['form_label_name'] = 'Super User Name'

    @classmethod
    def get_create_viewmodel(cls, site_user, title, form, modelstate):

        modelstate, modelstate_bool = SuperUser.get_modelstate(modelstate)

        viewmodel = Create_ViewModel(site_user, title, form, modelstate, modelstate_bool).viewmodel

        return viewmodel

class Details_Delete_ViewModel(BaseViewModel):
    def __init__(self, site_user, title, superuser):
        
        super().__init__(site_user, title)

        self.viewmodel['descriptive_list'] = 'superuser/descriptive_list.html' # app/shared_create.html params
        self.viewmodel['delete_url'] = 'superuser:delete'
        self.viewmodel['index_url'] = 'superuser:index'

        self.viewmodel['item'] = superuser # super_user/descriptive_list.html params
        self.viewmodel['list_label_name'] = 'Super User Name'
        self.viewmodel['list_label_email'] = 'E-mail'

    @classmethod
    def get_details_and_delete_viewmodel(cls, site_user, title, superuser_id):

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        viewmodel = Details_Delete_ViewModel(site_user, title, superuser).viewmodel

        return viewmodel
