from datetime import datetime

from django.db import models

from app.models import SiteUser, GroupOwner, GroupOwner_Choices
from app.mixins import HelperMixins

from groupowner.forms import GroupOwnerForm_Create, GroupOwnerForm_Transfer

class BaseViewModel(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, groupowners, filter):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'groupowner-id' # app/shared_index.html params
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate'] =  modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html' 
        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']
        self.viewmodel['create_url'] = 'groupowner:create'
        self.viewmodel['create_url_html'] = 'groupowner/create_url.html'
        self.viewmodel['create_name'] = 'Create Group Owner'
        self.viewmodel['index_table'] = 'groupowner/index_table.html'
        self.viewmodel['filter'] = filter

        self.viewmodel['items'] = groupowners # super_user/index_table.html params
        self.viewmodel['header_label_item'] = 'Super User Name'
        self.viewmodel['item_url'] = 'poolgroup:index'
        self.viewmodel['transfer_url'] = 'groupowner:transfer' 
        self.viewmodel['details_url'] = 'groupowner:details' 
        self.viewmodel['delete_url'] = 'groupowner:delete'
 

    @classmethod
    def get_index_viewmodel(cls, site_user, title, filter, modelstate):

        modelstate, modelstate_bool = GroupOwner.get_modelstate(modelstate)
        groupowners = GroupOwner.get_all_items(GroupOwner)

        viewmodel = Index_ViewModel(site_user, title, modelstate, modelstate_bool, groupowners, filter).viewmodel

        return viewmodel

class Create_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, form, modelstate, modelstate_bool, filter):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'groupowner-id' # shared_create params
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['create_edit_form_html'] = 'groupowner/create_edit_form.html' 
        self.viewmodel['form_url'] = 'groupowner:create'
        self.viewmodel['form_html'] = 'groupowner/groupowner_form.html'
        self.viewmodel['index_url'] = 'groupowner:index'
        self.viewmodel['index_url_html'] = 'groupowner/index_url.html'
        self.viewmodel['filter'] = filter
        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

        self.viewmodel['form'] = form # groupowner_form params
        self.viewmodel['form_label_name'] = 'Group Owner Name'
        self.viewmodel['form_label_email'] = 'Group Owner E-Mail'

    @classmethod
    def get_create_viewmodel(cls, site_user, title, filter, modelstate):

        modelstate, modelstate_bool = GroupOwner.get_modelstate(modelstate)

        form = GroupOwnerForm_Create(initial = {'filter':filter})

        viewmodel = Create_ViewModel(site_user, title, form, modelstate, modelstate_bool, filter).viewmodel

        return viewmodel

class Transfer_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, form, modelstate, modelstate_bool, groupowner_id, filter):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'groupowner-id' # shared_create params
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['create_edit_form_html'] = 'groupowner/transfer_form.html' 
        self.viewmodel['form_url'] = 'groupowner:transfer'
        self.viewmodel['form_html'] = 'groupowner/transfer_ownership_form.html'
        self.viewmodel['index_url'] = 'groupowner:index'
        self.viewmodel['index_url_html'] = 'groupowner/index_url.html'
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter
        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

        self.viewmodel['form'] = form # groupowner_form params
        self.viewmodel['form_label_name'] = 'Existing Group Owner'
        self.viewmodel['form_label_new_groupowner'] = 'New Group Owner'
        self.viewmodel['form_label_submit'] = 'Transfer'

    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, groupowner_id, filter, modelstate):

        modelstate, modelstate_bool = GroupOwner.get_modelstate(modelstate)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)
        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)
        GroupOwner_Choices.get_groupowner_choices()

        form = GroupOwnerForm_Transfer(instance = groupowner, initial = {'filter':filter})

        viewmodel = Transfer_ViewModel(site_user, title, form, modelstate, modelstate_bool, groupowner_id, filter).viewmodel

        return viewmodel

class Details_Delete_ViewModel(BaseViewModel):
    def __init__(self, site_user, title, groupowner, filter, modelstate, modelstate_bool):
        
        super().__init__(site_user, title)

        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate'] =  modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html' 
        self.viewmodel['descriptive_list'] = 'groupowner/descriptive_list.html' # app/shared_create.html params
        self.viewmodel['delete_url'] = 'groupowner:delete'
        self.viewmodel['delete_form'] = 'groupowner/delete_form.html'
        self.viewmodel['index_url'] = 'groupowner:index'
        self.viewmodel['edit_index_url_html'] = 'groupowner/index_url_2.html'
        self.viewmodel['groupowner_id'] = groupowner.id
        self.viewmodel['filter'] = filter

        self.viewmodel['item'] = groupowner # groupowner/descriptive_list.html params
        self.viewmodel['form_label_name'] = 'Group Owner Name'
        self.viewmodel['form_label_email'] = 'E-mail'

    @classmethod
    def get_details_and_delete_viewmodel(cls, site_user, title, groupowner_id, filter, modelstate):

        modelstate, modelstate_bool = GroupOwner.get_modelstate(modelstate)

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)

        viewmodel = Details_Delete_ViewModel(site_user, title, groupowner, filter, modelstate, modelstate_bool).viewmodel

        return viewmodel
