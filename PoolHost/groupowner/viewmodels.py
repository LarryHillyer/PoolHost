from datetime import datetime

from django.db import models

from app.models import SiteUser, GroupOwner
from app.mixins import HelperMixins

class BaseViewModel(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, groupowners):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'groupowner-id' # app/shared_index.html params
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate'] =  modelstate
        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']
        self.viewmodel['create_url'] = 'groupowner:create'
        self.viewmodel['create_name'] = 'Create Group Owner'
        self.viewmodel['index_table'] = 'groupowner/index_table.html'

        self.viewmodel['items'] = groupowners # super_user/index_table.html params
        self.viewmodel['header_label_item'] = 'Super User Name'
        self.viewmodel['item_url'] = 'poolgroup:index' 
        self.viewmodel['details_url'] = 'groupowner:details' 
        self.viewmodel['delete_url'] = 'groupowner:delete'
 

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelstate_bool = GroupOwner.get_modelstate(modelstate)
        groupowners = GroupOwner.get_all_items(GroupOwner)

        viewmodel = Index_ViewModel(site_user, title, modelstate, modelstate_bool, groupowners).viewmodel

        return viewmodel

class Create_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, form, modelstate, modelstate_bool):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'groupowner-id' # shared_create params
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['form_url'] = 'groupowner:create'
        self.viewmodel['form_html'] = 'groupowner/groupowner_form.html'
        self.viewmodel['index_url'] = 'groupowner:index'
        self.viewmodel['scripts'] = ['app/scripts/jqueryvalidate.js']

        self.viewmodel['form'] = form # groupowner_form params
        self.viewmodel['form_label_name'] = 'Group Owner Name'
        self.viewmodel['form_label_email'] = 'Group Owner E-Mail'

    @classmethod
    def get_create_viewmodel(cls, site_user, title, form, modelstate):

        modelstate, modelstate_bool = GroupOwner.get_modelstate(modelstate)

        viewmodel = Create_ViewModel(site_user, title, form, modelstate, modelstate_bool).viewmodel

        return viewmodel

class Details_Delete_ViewModel(BaseViewModel):
    def __init__(self, site_user, title, groupowner):
        
        super().__init__(site_user, title)

        self.viewmodel['descriptive_list'] = 'groupowner/descriptive_list.html' # app/shared_create.html params
        self.viewmodel['delete_url'] = 'groupowner:delete'
        self.viewmodel['index_url'] = 'groupowner:index'

        self.viewmodel['item'] = groupowner # groupowner/descriptive_list.html params
        self.viewmodel['form_label_name'] = 'Group Owner Name'
        self.viewmodel['form_label_email'] = 'E-mail'

    @classmethod
    def get_details_and_delete_viewmodel(cls, site_user, title, groupowner_id):

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)

        viewmodel = Details_Delete_ViewModel(site_user, title, groupowner).viewmodel

        return viewmodel
