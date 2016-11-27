from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolOwner, PoolGroup, GroupOwner, SuperUser 
from app.models import GroupOwner_Choices, PoolGroup_Choices
from app.mixins import HelperMixins

from poolowner.forms import PoolOwnerForm_SuperUser_Create, PoolOwnerForm_SuperUser_Edit
from poolowner.forms import PoolOwnerForm_GroupOwner_Create, PoolOwnerForm_GroupOwner_Edit

class BaseViewModel(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year}
        pass

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolowners, filter,
        poolgroup_id, groupowner_id):

        super().__init__(site_user, title)
     
        self.viewmodel['partial_view_id'] = 'poolowner-id' # app/shared_index_pagination.html params
        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter' ] = filter
        self.viewmodel['modelstate'] = modelstate 
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html' 
        self.viewmodel['create_url'] = 'poolowner:create'
        self.viewmodel['create_url_html'] =  'poolowner/create_url.html' 
        self.viewmodel['create_name'] = 'Create Pool Owner' 
        self.viewmodel['index_table'] = 'poolowner/index_table.html' 
        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']
 
        self.viewmodel['items'] = poolowners # poolgroup/index_table.html params
        self.viewmodel['header_label_item'] = 'Pool Owner'
        self.viewmodel['header_label_poolgroup'] = 'Pool Group'
        self.viewmodel['item_url'] = 'pool:index'
        self.viewmodel['edit_url'] = 'poolowner:edit'
        self.viewmodel['details_url'] = 'poolowner:details' 
        self.viewmodel['delete_url'] = 'poolowner:delete' 
                        

    @classmethod
    def get_viewmodel_parameters_by_state(cls,  filter, poolgroup_id, groupowner_id):

        if filter == 0:

            groupowner_id = 0
            poolgroup_id = 0

            poolowners = PoolOwner.get_all_items(PoolOwner)

        elif filter == 1:

            if groupowner_id == 0:     
                groupowners = GroupOwner.get_all_items(GroupOwner)
                groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)                       

            poolowners = Index_ViewModel.filter_poolowners(groupowner_id, poolgroup_id)

        elif filter == 2:

            if poolgroup_id == 0:
                poolgroups = PoolGroup.get_all_items(PoolGroup)
                poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)

            poolowners = Index_ViewModel.filter_poolowners(groupowner_id, poolgroup_id)

        elif filter == 3:

            if groupowner_id == 0:     
                groupowners = GroupOwner.get_all_items(GroupOwner)
                groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)                       


            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
            poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)
            
            poolowners = Index_ViewModel.filter_poolowners(groupowner_id, poolgroup_id)

        return groupowner_id, poolgroup_id, poolowners


    @classmethod
    def filter_poolowners(cls, groupowner_id = 0, poolgroup_id = 0,):

        if poolgroup_id != 0:
            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        elif groupowner_id != 0:
            poolowners = PoolOwner.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        
        return poolowners

class Create_Edit_ViewModel(BaseViewModel):
    def __init__(self, site_user, title, modelstate, modelstate_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'poolowner-id' # shared_create params
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['create_edit_form_html'] = 'poolowner/create_edit_form.html'
        self.viewmodel['form_html'] = 'poolowner/poolowner_form.html'
        self.viewmodel['form_url'] = 'poolowner:create'
        self.viewmodel['index_url'] = 'poolowner:index'
        self.viewmodel['index_url_html'] = 'poolowner/index_url.html'
        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter
        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js', 'app/scripts/Client/GOwner_PGroup_CDD.js']

        self.viewmodel['form'] = form # poolowner/poolowner_form.html
        self.viewmodel['form_label_name'] = 'Pool Owner'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'
        self.viewmodel['form_label_poolgroup'] = 'Pool Group'
        self.viewmodel['form_label_submit'] = submit_label

class SuperUser_Index(Index_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolowners, poolgroups, groupowners, filter,
        poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelstate_bool, poolowners, filter,
            poolgroup_id, groupowner_id) 

        self.viewmodel['use_pagination'] = True  # app/shared_index_pagination.html          
        self.viewmodel['pagination'] = 'app/user_navigation.html'  

        self.viewmodel['superuser_pagination'] = 'poolowner/superuser_pagination.html' #app/user_navigation.html
        self.viewmodel['groupowner_pagination'] = 'poolowner/groupowner_pagination.html'
        self.viewmodel['shared_groupowner_pagination'] = 'app/groupowner_pagination.html'
        self.viewmodel['groupowner_pagination_url_html'] = 'poolowner/groupowner_pagination_url.html'
        self.viewmodel['shared_poolgroup_pagination'] = 'app/poolgroup_pagination.html'
        self.viewmodel['poolgroup_pagination_url_html'] = 'poolowner/poolgroup_pagination_url.html'
        self.viewmodel['shared_poolowner_pagination'] = 'app/poolowner_pagination.html'
        self.viewmodel['poolowner_pagination_url_html'] = 'poolowner/poolowner_pagination_url.html'
                       
        self.viewmodel['index_url'] = 'poolowner:index' #poolowner/superuser_pagination.html
        
        self.viewmodel['poolgroups'] = poolgroups #app/poolgroup_pagination
        self.viewmodel['groupowners'] = groupowners #app/groupowner_pagination
        
        self.viewmodel['header_label_groupowner'] = 'Group Owner Name' # poolowner/index_table.html
        self.viewmodel['transfer_url'] = 'poolgroup:transfer' 

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id, poolgroup_id, poolowners = Index_ViewModel.get_viewmodel_parameters_by_state(filter, poolgroup_id, groupowner_id)
        
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowner_id == 0:
            poolgroups = PoolGroup.get_all_items(PoolGroup)
        else:
            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelstate_bool, 
            poolowners, poolgroups, groupowners, filter, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class SuperUser_Create(Create_Edit_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelstate_bool, form, filter,
            poolgroup_id, groupowner_id, submit_label)
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)
        GroupOwner_Choices.get_groupowner_choices()

        poolgroups = PoolGroup.get_all_items(PoolGroup)
        if poolgroups.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Pool Group First!'}
            return viewmodel

        poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)
        PoolGroup_Choices.get_poolgroup_choices_by_groupowner_id(groupowner_id)

        form = PoolOwnerForm_SuperUser_Create(initial={'poolgroup_id': poolgroup_id,
                                                        'groupowner_id' : groupowner_id,
                                                        'filter' : filter})

        submit_label = 'Create'
        viewmodel = SuperUser_Create(site_user, title, modelstate, modelstate_bool, form, filter, 
            poolgroup_id, groupowner_id, submit_label).viewmodel
        
        return viewmodel
