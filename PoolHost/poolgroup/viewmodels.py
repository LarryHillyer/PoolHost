from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolGroup, GroupOwner, SuperUser, GroupOwner_Choices
from app.mixins import HelperMixins

from poolgroup.forms import PoolGroupForm_SuperUser_Create, PoolGroupForm_SuperUser_Edit, PoolGroupForm_SuperUser_Transfer
from poolgroup.forms import PoolGroupForm_GroupOwner_Create, PoolGroupForm_GroupOwner_Edit


class BaseViewModel(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year}
        pass

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolgroups, filter,
        groupowner_id):

        super().__init__(site_user, title)
     
        self.viewmodel['partial_view_id'] = 'poolgroup-id' # app/shared_index_pagination.html params
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter' ] = filter
        self.viewmodel['modelstate'] = modelstate 
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html' 
        self.viewmodel['create_url'] = 'poolgroup:create'
        self.viewmodel['create_url_html'] =  'poolgroup/create_url.html' 
        self.viewmodel['create_name'] = 'Create Pool Group' 
        self.viewmodel['index_table'] = 'poolgroup/index_table.html' 
        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']
 
        self.viewmodel['items'] = poolgroups # poolgroup/index_table.html params
        self.viewmodel['header_label_item'] = 'Pool Group Name'
        self.viewmodel['item_url'] = 'poolowner:index'
        self.viewmodel['edit_url'] = 'poolgroup:edit'
        self.viewmodel['details_url'] = 'poolgroup:details' 
        self.viewmodel['delete_url'] = 'poolgroup:delete' 
                        
    @classmethod
    def get_poolgroups_by_groupowners(cls, filter, groupowner_id):

        if filter == 0:
            groupowner_id = 0
            poolgroups = PoolGroup.get_all_items(PoolGroup)

        elif filter == 1:

            if groupowner_id == 0:     
                groupowners = GroupOwner.get_all_items(GroupOwner)
            else:
                groupowners = GroupOwner.get_items_by_id(GroupOwner, groupowner_id)
            
            groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)       

            if groupowner_id != 0:
                poolgroups = Index_ViewModel.filter_poolgroups(groupowner_id)

        return groupowner_id, poolgroups

    @classmethod
    def filter_poolgroups(cls, groupowner_id = 0, poolgroup_id = 0,):

        if poolgroup_id != 0:
            poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)
        elif groupowner_id != 0:
            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        
        return poolgroups

class Create_Edit_ViewModel(BaseViewModel):
    def __init__(self, site_user, title, modelstate, modelstate_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'poolgroup-id' # shared_create params
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['create_edit_form_html'] = 'poolgroup/create_edit_form.html'
        self.viewmodel['form_html'] = 'poolgroup/poolgroup_form.html'
        self.viewmodel['form_url'] = 'poolgroup:create'
        self.viewmodel['index_url'] = 'poolgroup:index'
        self.viewmodel['index_url_html'] = 'poolgroup/index_url.html'
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter
        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

        self.viewmodel['form'] = form # poolgroup/poolgroup_form.html
        self.viewmodel['form_label_name'] = 'Pool Group Name'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'
        self.viewmodel['form_label_submit'] = submit_label

class Details_Delete_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolgroup,  
        filter, groupowner_id):

        super().__init__(site_user, title)

        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['descriptive_list'] = 'poolgroup/descriptive_list.html' # app/shared_create.html params
        self.viewmodel['delete_url'] = 'poolgroup:delete'
        self.viewmodel['delete_form'] = 'poolgroup/delete_form.html'
        self.viewmodel['index_url'] = 'poolgroup:index'
        self.viewmodel['edit_url'] = 'poolgroup:edit'
        self.viewmodel['edit_index_url_html'] = 'poolgroup/edit_index_url.html'
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['poolgroup_id'] = poolgroup.id
        self.viewmodel['filter'] = filter

        self.viewmodel['item'] = poolgroup # poolgroup/descriptive_list.html params
        self.viewmodel['item_label_name'] = 'Pool Group'
        self.viewmodel['item_label_groupowner_name'] = 'Group Owner'

class SuperUser_Index(Index_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolgroups, groupowners, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelstate_bool, poolgroups, filter,
            groupowner_id) 

        self.viewmodel['use_pagination'] = True  # app/shared_index_pagination.html          
        self.viewmodel['pagination'] = 'app/user_navigation.html'  

        self.viewmodel['superuser_pagination'] = 'poolgroup/superuser_pagination.html' #app/user_navigation.html
        self.viewmodel['groupowner_pagination'] = 'poolgroup/groupowner_pagination.html'
        self.viewmodel['shared_groupowner_pagination'] = 'app/groupowner_pagination.html'
        self.viewmodel['groupowner_pagination_url_html'] = 'poolgroup/groupowner_pagination_url.html'
        self.viewmodel['shared_poolgroup_pagination'] = 'app/poolgroup_pagination.html'
        self.viewmodel['shared_poolowner_pagination'] = 'app/poolowner_pagination.html'
                       
        self.viewmodel['index_url'] = 'poolgroup:index' #poolgroup/superuser_pagination.html
        
        self.viewmodel['groupowners'] = groupowners #app/groupowner_pagination
        self.viewmodel['groupowner_id'] = groupowner_id

        self.viewmodel['header_label_groupowner'] = 'Group Owner Name' # poolgroup/index_table.html
        self.viewmodel['transfer_url'] = 'poolgroup:transfer' 

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id, poolgroups = Index_ViewModel.get_poolgroups_by_groupowners(filter, groupowner_id)
        
        groupowners = GroupOwner.get_all_items(GroupOwner) 

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelstate_bool, poolgroups, groupowners, filter, groupowner_id).viewmodel
        
        return viewmodel

class GroupOwner_Index(Index_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolgroups, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelstate_bool, poolgroups, filter,
            groupowner_id) 

        self.viewmodel['use_pagination'] = False  # app/shared_index_pagination.html          

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter = None):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        viewmodel = GroupOwner_Index(site_user, title, modelstate, modelstate_bool, poolgroups, filter, groupowner_id).viewmodel
        
        return viewmodel

class SuperUser_Create(Create_Edit_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelstate_bool, form, filter,
            groupowner_id, submit_label)
        self.viewmodel['form_url'] = 'poolgroup:create'
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)
        GroupOwner_Choices.get_groupowner_choices()

        form = PoolGroupForm_SuperUser_Create(initial={'groupowner_id' : groupowner_id,
                                                        'filter' : filter})

        submit_label = 'Create'
        viewmodel = SuperUser_Create(site_user, title, modelstate, modelstate_bool, form, filter, 
            groupowner_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Edit(Create_Edit_ViewModel):
    def __init__(self, site_user, title, modelstate, modelstate_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelstate_bool, form, filter,
            groupowner_id, submit_label)
        self.viewmodel['form_url'] = 'poolgroup:edit'

    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        groupowner_id = poolgroup.groupowner_id
        GroupOwner_Choices.get_groupowner_choices(groupowner_id)
        
        form = PoolGroupForm_SuperUser_Edit(instance = poolgroup, initial = {'filter':filter})

        submit_label = 'Edit'
        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelstate_bool, form, filter, 
            groupowner_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Transfer(BaseViewModel):
    def __init__(self, site_user, title, form, modelstate, modelstate_bool, poolgroup, groupowner_id, filter):
        
        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'poolgroup-id' # shared_create params
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_bool'] = modelstate_bool
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'
        self.viewmodel['create_edit_form_html'] = 'poolgroup/transfer_form.html' 
        self.viewmodel['form_url'] = 'poolgroup:transfer'
        self.viewmodel['form_html'] = 'poolgroup/transfer_ownership_form.html'
        self.viewmodel['index_url'] = 'poolgroup:index'
        self.viewmodel['index_url_html'] = 'poolgroup/index_url.html'
        self.viewmodel['poolgroup_id'] = poolgroup.id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter
        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

        self.viewmodel['form'] = form # poolgroup_form params
        self.viewmodel['poolgroup_label_name'] = 'Pool Group'
        self.viewmodel['poolgroup_name'] = poolgroup.name
        self.viewmodel['poolgroup_label_groupowner'] = 'Existing Group Owner'
        self.viewmodel['poolgroup_groupowner_name'] = poolgroup.groupowner.name
        self.viewmodel['form_label_new_groupowner'] = 'New Group Owner'
        self.viewmodel['form_label_submit'] = 'Transfer'

    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, poolgroup_id, groupowner_id, filter, modelstate):

        modelstate, modelstate_bool = GroupOwner.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, poolgroup.groupowner_id)
        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)
        GroupOwner_Choices.get_groupowner_choices()

        form = PoolGroupForm_SuperUser_Transfer(initial = {'filter':filter,
                                                            'groupowner_id': poolgroup.groupowner_id})

        viewmodel = SuperUser_Transfer(site_user, title, form, modelstate, modelstate_bool, poolgroup, groupowner_id, filter).viewmodel

        return viewmodel
       
class GroupOwner_Create(Create_Edit_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelstate_bool, form, filter,
            groupowner_id, submit_label) 

        self.viewmodel['form_url'] = 'poolgroup:create'

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        form = PoolGroupForm_GroupOwner_Create(initial = {'groupowner_id' : groupowner_id,
                                                           'filter': filter})

        submit_label = 'Create'
        viewmodel = GroupOwner_Create(site_user, title, modelstate, modelstate_bool, form, filter, 
            groupowner_id, submit_label).viewmodel
        
        return viewmodel

class GroupOwner_Edit(Create_Edit_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelstate_bool, form, filter,
            groupowner_id, submit_label)

        self.viewmodel['form_url'] = 'poolgroup:edit'

    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)
        
        form = PoolGroupForm_GroupOwner_Edit(instance = poolgroup, 
                                                initial = {'groupowner_id': groupowner_id,
                                                            'filter': filter})

        submit_label = 'Edit'
        viewmodel = GroupOwner_Edit(site_user, title, modelstate, modelstate_bool, form, filter, 
            groupowner_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_Delete_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolgroup, 
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelstate_bool, poolgroup, 
            filter, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, 
        groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)
        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelstate_bool, 
            poolgroup, filter, groupowner_id).viewmodel
        
        return viewmodel

class GroupOwner_Details(Details_Delete_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolgroup, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelstate_bool, poolgroup, filter,
            groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = GroupOwner_Details(site_user, title, modelstate, modelstate_bool, 
            poolgroup, filter, groupowner_id).viewmodel
        
        return viewmodel

class User_Delete(Details_Delete_ViewModel):

    def __init__(self, site_user, title, modelstate, modelstate_bool, poolgroup, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelstate_bool, poolgroup, filter,
            groupowner_id) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter,
        groupowner_id):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelstate_bool, poolgroup, 
            filter, groupowner_id).viewmodel
        
        return viewmodel
