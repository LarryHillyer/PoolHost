from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolGroup, GroupOwner, SuperUser, GroupOwner_Choices, PoolGroup_Choices
from app.mixins import HelperMixins

from poolgroup.forms import PoolGroupForm_Create, PoolGroupForm_Edit, PoolGroupForm_Transfer

class BaseViewModel(object):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,
                            'modelsuccess_bool': modelsuccess_bool,
                            'modelstate': modelstate,
                            'modelstate_html': 'app/modelstatus.html' }


class Table_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroups, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
     
        self.viewmodel['partial_view_id'] = 'poolgroup-id' # app/shared_index_pagination.html params

        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter' ] = filter

        self.viewmodel['create_url'] = 'poolgroup:create'
        self.viewmodel['create_link_name'] = 'Create Pool Group'
        self.viewmodel['create_link_html'] =  'poolgroup/create_link.html' 
 
        self.viewmodel['index_table_html'] = 'poolgroup/index_table.html' 
 
        self.viewmodel['items'] = poolgroups # poolgroup/index_table.html params
        self.viewmodel['header_label_item'] = 'Pool Group Name'
        self.viewmodel['item_url'] = 'poolowner:index'
        self.viewmodel['transfer_url'] = 'poolgroup:transfer' 
        self.viewmodel['edit_url'] = 'poolgroup:edit'
        self.viewmodel['details_url'] = 'poolgroup:details' 
        self.viewmodel['delete_url'] = 'poolgroup:delete' 

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']
                        
class Form_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
        
        self.viewmodel['partial_view_id'] = 'poolgroup-id' 

        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form 
        self.viewmodel['form_label_submit'] = submit_label

        self.viewmodel['index_url'] = 'poolgroup:index'
        self.viewmodel['index_link_html'] = 'poolgroup/index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class DescriptiveList_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'superuser-id' # shared_create params

        self.viewmodel['poolgroup_id'] = poolgroup.id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['descriptive_list'] = 'poolgroup/descriptive_list.html' # app/shared_create.html params

        self.viewmodel['item'] = poolgroup # poolgroup/descriptive_list.html params
        self.viewmodel['item_label_name'] = 'Pool Group'
        self.viewmodel['item_label_groupowner_name'] = 'Group Owner'

        self.viewmodel['index_url'] = 'poolgroup:index'


class Pagination_Routing_ViewModel(Table_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroups, filter,
            groupowner_id)
 
        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['superuser_pagination_list_html'] = 'poolgroup/superuser_pagination_list.html' 
        self.viewmodel['groupowner_pagination_list_html'] = 'poolgroup/groupowner_pagination_list.html'

        self.viewmodel['shared_groupowner_pagination_list_html'] = 'app/shared_groupowner_pagination_list.html'
        self.viewmodel['shared_poolgroup_pagination_list_html'] = 'app/shared_poolgroup_pagination_list.html'
        self.viewmodel['shared_poolowner_pagination_list_html'] = 'app/shared_poolowner_pagination_list.html'

        self.viewmodel['groupowner_pagination_link_html'] = 'poolgroup/groupowner_pagination_link.html'
        self.viewmodel['poolgroup_pagination_link_html'] = 'poolgroup/poolgroup_pagination_link.html'
        self.viewmodel['poolowner_pagination_link_html'] = 'poolgroup/poolowner_pagination_link.html'


        self.viewmodel['index_url'] = 'poolgroup:index'
                             
        self.viewmodel['groupowners'] = groupowners

class Create_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id, submit_label)
        
        self.viewmodel['form_template_html'] = 'poolgroup/create_form.html'
        self.viewmodel['form_html'] = 'poolgroup/poolgroup_form.html'
        self.viewmodel['form_url'] = 'poolgroup:create'

        self.viewmodel['form_label_name'] = 'Pool Group'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'

class Edit_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id, submit_label)
        
        self.viewmodel['poolgroup_id'] = poolgroup_id

        self.viewmodel['form_template_html'] = 'poolgroup/edit_form.html'
        self.viewmodel['form_html'] = 'poolgroup/poolgroup_form.html'
        self.viewmodel['form_url'] = 'poolgroup:edit'

        self.viewmodel['form_label_name'] = 'Pool Group'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'

class Transfer_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool,  form,
         filter, poolgroup, groupowner_id, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, 
            filter, groupowner_id,  submit_label)

        self.viewmodel['poolgroup_id'] = poolgroup.id

        self.viewmodel['form_template_html'] = 'poolgroup/transfer_form.html' 
        self.viewmodel['form_url'] = 'poolgroup:transfer'
        self.viewmodel['form_html'] = 'poolgroup/transfer_ownership_form.html'

        self.viewmodel['form_name'] = poolgroup.name
        self.viewmodel['form_label_name'] = 'Existing Pool Owner'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'
        self.viewmodel['form_groupowner_name'] = poolgroup.groupowner.name
        self.viewmodel['form_label_new_groupowner'] = 'New Group Owner'

class Details_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id)

        self.viewmodel['edit_url'] = 'poolgroup:edit'
        self.viewmodel['details_links_html'] = 'poolgroup/details_links.html'

class Delete_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id)

        self.viewmodel['delete_url'] = 'poolgroup:delete'
        self.viewmodel['delete_form'] = 'poolgroup/delete_form.html'


class SuperUser_Index(Pagination_Routing_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter, 
            groupowner_id) 

        self.viewmodel['use_pagination'] = True  # app/shared_index_pagination.html          

        self.viewmodel['header_label_groupowner'] = 'Group Owner Name' # poolgroup/index_table.html


    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id, poolgroups = SuperUser_Index.get_viewmodel_parameters_by_state(filter, groupowner_id)
        
        groupowners = GroupOwner.get_all_items(GroupOwner) 

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter, groupowner_id).viewmodel
        
        return viewmodel

    @classmethod
    def get_viewmodel_parameters_by_state(cls, filter, groupowner_id):

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
                poolgroups = SuperUser_Index.filter_poolgroups(groupowner_id)

        return groupowner_id, poolgroups

    @classmethod
    def filter_poolgroups(cls, groupowner_id = 0, poolgroup_id = 0,):

        if poolgroup_id != 0:
            poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)
        elif groupowner_id != 0:
            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        
        return poolgroups

class SuperUser_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id, submit_label)
        self.viewmodel['form_url'] = 'poolgroup:create'
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)
        GroupOwner_Choices.get_groupowner_choices()

        form = PoolGroupForm_Create(initial={'groupowner_id' : groupowner_id,
                                                        'filter' : filter})

        submit_label = 'Create'
        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            groupowner_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Edit(Edit_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolgroup_id, groupowner_id, submit_label)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        groupowner_id = poolgroup.groupowner_id
        GroupOwner_Choices.get_groupowner_choices()
        
        form = PoolGroupForm_Edit(instance = poolgroup, initial = {'filter':filter})

        submit_label = 'Edit'
        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolgroup_id, groupowner_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Transfer(Transfer_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup, groupowner_id,  submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,  filter,
            poolgroup, groupowner_id, submit_label)

    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, filter, poolgroup_id, groupowner_id, 
            modelstate):

        modelstate, modelsuccess_bool = GroupOwner.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)
        
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, poolgroup.groupowner_id)

        GroupOwner_Choices.get_groupowner_choices_2(groupowner_id)
        groupowner_choices = GroupOwner_Choices.get_all_items(GroupOwner_Choices)

        form = PoolGroupForm_Transfer(initial = {'filter':filter,
                                                            'name': poolgroup.name,
                                                            'groupowner_name': poolgroup.groupowner.name,
                                                            'new_groupowner_id': groupowner_choices[0].groupowner_id})

        submit_label = 'Transfer'

        viewmodel = SuperUser_Transfer(site_user, title, modelstate, modelsuccess_bool, form,  filter, poolgroup, 
            groupowner_id, submit_label).viewmodel

        return viewmodel

class SuperUser_Details(Details_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup, 
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup, 
            filter, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, 
        groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)
        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, 
            poolgroup, filter, groupowner_id).viewmodel
        
        return viewmodel


class GroupOwner_Index(Table_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroups, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroups, filter,
            groupowner_id) 

        self.viewmodel['use_pagination'] = False  # app/shared_index_pagination.html          

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter = None):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        viewmodel = GroupOwner_Index(site_user, title, modelstate, modelsuccess_bool, poolgroups, filter, groupowner_id).viewmodel
        
        return viewmodel
       
class GroupOwner_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id, submit_label) 

        self.viewmodel['form_url'] = 'poolgroup:create'

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        form = PoolGroupForm_Create(initial = {'groupowner_id' : groupowner_id,
                                                           'filter': filter})

        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        submit_label = 'Create'
        viewmodel = GroupOwner_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            groupowner_id, submit_label).viewmodel
        
        return viewmodel

class GroupOwner_Edit(Edit_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolgroup_id, groupowner_id, submit_label)

        self.viewmodel['form_url'] = 'poolgroup:edit'

    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)
        
        form = PoolGroupForm_Edit(instance = poolgroup, 
                                                initial = {'groupowner_id': groupowner_id,
                                                            'filter': filter})

        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        submit_label = 'Edit'
        viewmodel = GroupOwner_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolgroup_id, groupowner_id, submit_label).viewmodel
        
        return viewmodel

class GroupOwner_Details(Details_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
            groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = GroupOwner_Details(site_user, title, modelstate, modelsuccess_bool, 
            poolgroup, filter, groupowner_id).viewmodel
        
        return viewmodel


class User_Delete(Delete_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
            groupowner_id) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, poolgroup_id, filter,
        groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelsuccess_bool, poolgroup, 
            filter, groupowner_id).viewmodel
        
        return viewmodel
