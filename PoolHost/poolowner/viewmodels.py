from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolOwner, PoolGroup, GroupOwner, SuperUser 
from app.models import GroupOwner_Choices, PoolGroup_Choices, PoolOwner_Choices
from app.mixins import HelperMixins

from poolowner.forms import PoolOwnerForm_Create, PoolOwnerForm_Transfer

class BaseViewModel(object):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool,):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,
                            'modelsuccess_bool': modelsuccess_bool,
                            'modelstate': modelstate,
                            'modelstate_html': 'app/modelstatus.html' }


class Table_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolowners, filter,
        poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
     
        self.viewmodel['partial_view_id'] = 'poolowner-id' # app/shared_index_pagination.html params

        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter' ] = filter

        self.viewmodel['create_url'] = 'poolowner:create'
        self.viewmodel['create_link_name'] = 'Create Pool Owner'
        self.viewmodel['create_link_html'] =  'poolowner/create_link.html' 

        self.viewmodel['index_table_html'] = 'poolowner/index_table.html' 
 
        self.viewmodel['items'] = poolowners # poolowner/index_table.html params
        self.viewmodel['header_label_item'] = 'Pool Owner'
        self.viewmodel['header_label_poolgroup'] = 'Pool Group'
        self.viewmodel['item_url'] = 'pool:index'
        self.viewmodel['transfer_url'] = 'poolowner:transfer' 
        self.viewmodel['details_url'] = 'poolowner:details' 
        self.viewmodel['delete_url'] = 'poolowner:delete' 

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']
                        
class Form_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
        
        self.viewmodel['partial_view_id'] = 'poolowner-id' # shared_create params

        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form # poolowner/poolowner_form.html
        self.viewmodel['form_label_submit'] = submit_label

        self.viewmodel['index_url'] = 'poolowner:index'
        self.viewmodel['index_link_html'] = 'poolowner/index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js', 'app/scripts/Client/GOwner_PGroup_CDD.js']

class DescriptiveList_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'superuser-id' # shared_create params

        self.viewmodel['poolowner_id'] = poolowner.id
        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['descriptive_list'] = 'poolowner/descriptive_list.html' # app/shared_create.html params

        self.viewmodel['item'] = poolowner # poolgroup/descriptive_list.html params
        self.viewmodel['item_label_name'] = 'Pool Owner'
        self.viewmodel['item_label_poolgroup_name'] = 'Pool Group'
        self.viewmodel['item_label_groupowner_name'] = 'Group Owner'

        self.viewmodel['index_url'] = 'poolowner:index'


class Pagination_Routing_ViewModel(Table_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolowners, poolgroups, groupowners, filter,
        poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolowners, filter,
            poolgroup_id, groupowner_id)
 
        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['superuser_pagination_list_html'] = 'poolowner/superuser_pagination_list.html' 
        self.viewmodel['groupowner_pagination_list_html'] = 'poolowner/groupowner_pagination_list.html'

        self.viewmodel['shared_groupowner_pagination_list_html'] = 'app/shared_groupowner_pagination_list.html'
        self.viewmodel['shared_poolgroup_pagination_list_html'] = 'app/shared_poolgroup_pagination_list.html'
        self.viewmodel['shared_poolowner_pagination_list_html'] = 'app/shared_poolowner_pagination_list.html'

        self.viewmodel['groupowner_pagination_link_html'] = 'poolowner/groupowner_pagination_link.html'
        self.viewmodel['poolgroup_pagination_link_html'] = 'poolowner/poolgroup_pagination_link.html'
        self.viewmodel['poolowner_pagination_link_html'] = 'poolowner/poolowner_pagination_link.html'


        self.viewmodel['index_url'] = 'poolowner:index'
                             
        self.viewmodel['poolgroups'] = poolgroups 
        self.viewmodel['groupowners'] = groupowners

class Create_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolgroup_id, groupowner_id, submit_label)
        
        self.viewmodel['form_template_html'] = 'poolowner/create_form.html'
        self.viewmodel['form_html'] = 'poolowner/poolowner_form.html'
        self.viewmodel['form_url'] = 'poolowner:create'

        self.viewmodel['form_label_name'] = 'Pool Owner'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'
        self.viewmodel['form_label_poolgroup'] = 'Pool Group'

class Transfer_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter, poolowner,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolgroup_id, groupowner_id, submit_label)
        
        self.viewmodel['poolowner_id'] = poolowner.id

        self.viewmodel['form_template_html'] = 'poolowner/transfer_form.html' 
        self.viewmodel['form_url'] = 'poolowner:transfer'
        self.viewmodel['form_html'] = 'poolowner/transfer_ownership_form.html'

        self.viewmodel['form_label_name'] = 'Existing Pool Owner'
        self.viewmodel['form_label_poolgroup'] = 'Pool Group'
        self.viewmodel['form_label_new_poolowner'] = 'New Pool Owner'

class Details_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id)

        self.viewmodel['details_links_html'] = 'poolowner/details_links.html'
        self.viewmodel['transfer_url'] = 'poolowner:transfer'

class Delete_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id)

        self.viewmodel['delete_form'] = 'poolowner/delete_form.html'
        self.viewmodel['delete_url'] = 'poolowner:delete'


class SuperUser_Index(Pagination_Routing_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolowners, poolgroups, groupowners, filter,
        poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolowners,  poolgroups, groupowners, filter,
            poolgroup_id, groupowner_id) 

        self.viewmodel['use_pagination'] = True  # app/shared_index_pagination.html          
        
        self.viewmodel['header_label_groupowner'] = 'Group Owner' # poolowner/index_table.html


    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id, poolgroup_id, poolowners = SuperUser_Index.get_viewmodel_parameters_by_state(filter, poolgroup_id, groupowner_id)
        
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowner_id == 0:
            poolgroups = PoolGroup.get_all_items(PoolGroup)
        else:
            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, 
            poolowners, poolgroups, groupowners, filter, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

    @classmethod
    def get_viewmodel_parameters_by_state(cls,  filter, poolgroup_id, groupowner_id):

        if filter == 0:

            groupowner_id = 0
            poolgroup_id = 0

            poolowners = PoolOwner.get_all_items(PoolOwner)

        elif filter == 1:

            groupowners = GroupOwner.get_all_items(GroupOwner)
            if groupowner_id == 0:     
                groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)

            poolowners = PoolOwner.get_items_by_groupowner_id(PoolOwner, groupowner_id)

        elif filter == 2:
            poolgroups = PoolGroup.get_all_items(PoolGroup)
            if poolgroup_id == 0:
                poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)

            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)

        elif filter == 3:

            if groupowner_id == 0:
                groupowner_id = PoolGroup.get_item_by_id(PoolGroup,poolgroup_id).groupowner_id

            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
            if poolgroup_id == 0:
                poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)

            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
 
        return groupowner_id, poolgroup_id, poolowners


class SuperUser_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolgroup_id, groupowner_id, submit_label)
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

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

        form = PoolOwnerForm_Create(initial={'poolgroup_id': poolgroup_id,
                                                        'groupowner_id' : groupowner_id,
                                                        'filter' : filter})

        submit_label = 'Create'
        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolgroup_id, groupowner_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Transfer(Transfer_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolowner, poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolowner, poolgroup_id, groupowner_id, submit_label)
        
    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)

        PoolOwner_Choices.get_differentpoolowner_choices_by_poolgroup_id(poolowner.poolgroup_id, poolowner.id)
        poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
        if poolowner_choices.count() == 0:
            viewmodel = {'modelstate':'Error: No other poolowner is in pool group, add a pool owner to pool group first!'}
            return viewmodel

        form = PoolOwnerForm_Transfer(initial={'name' : poolowner.name,
                                                        'new_poolowner_id': poolowner_choices[0].poolowner_id,
                                                        'poolgroup_name': poolowner.poolgroup.name,
                                                        'filter' : filter})

        submit_label = 'Transfer'
        viewmodel = SuperUser_Transfer(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner, poolgroup_id, groupowner_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, 
        poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel


class GroupOwner_Index(Pagination_Routing_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolowners, poolgroups, groupowners, 
        filter, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolowners, poolgroups, groupowners, 
            filter, poolgroup_id, groupowner_id) 

        self.viewmodel['use_pagination'] = True  # app/shared_index_pagination.html          

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id
        groupowners = [GroupOwner.get_item_by_id(GroupOwner,groupowner_id)]
        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        poolgroup_id, poolowners = GroupOwner_Index.get_viewmodel_parameters_by_state(filter, poolgroup_id, 
            groupowner_id)

        viewmodel = GroupOwner_Index(site_user, title, modelstate, modelsuccess_bool, poolowners, poolgroups, 
            groupowners, filter, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

    @classmethod
    def get_viewmodel_parameters_by_state(cls,  filter, poolgroup_id, groupowner_id):

        if filter == 0:

            poolgroup_id = 0

            poolowners = PoolOwner.get_items_by_groupowner_id(PoolOwner, groupowner_id)

        elif filter == 1:

            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

            if poolgroup_id == 0:
                poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)

            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)

        return poolgroup_id, poolowners

class GroupOwner_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolgroup_id, groupowner_id, submit_label) 

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id
        GroupOwner_Choices.get_groupowner_choices(groupowner_id)

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        if poolgroups.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Pool Group First!'}
            return viewmodel

        poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)
        PoolGroup_Choices.get_poolgroup_choices_by_groupowner_id(groupowner_id)

        form = PoolOwnerForm_Create(initial = {'poolgroup_id': poolgroup_id,
                                                           'groupowner_id' : groupowner_id,
                                                           'filter': filter})

        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        submit_label = 'Create'
        viewmodel = GroupOwner_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolgroup_id, groupowner_id, submit_label).viewmodel
        
        return viewmodel

class GroupOwner_Transfer(Transfer_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolowner, poolgroup_id, groupowner_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolowner, poolgroup_id, groupowner_id, submit_label)
        
    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)
        PoolOwner_Choices.get_poolowner_choices_by_poolgroup_id(poolowner.poolgroup_id, poolowner.id)
        poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
        if poolowner_choices.count() == 0:
            viewmodel = {'modelstate':'Error: No other poolowner is in pool group, add a pool owner to pool group first!'}
            return viewmodel

        form = PoolOwnerForm_Transfer(initial={'name' : poolowner.name,
                                                        'new_poolowner_id': poolowner_choices[0].poolowner_id,
                                                        'poolgroup_name': poolowner.poolgroup.name,
                                                        'filter' : filter})

        submit_label = 'Transfer'
        viewmodel = GroupOwner_Transfer(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner, poolgroup_id, groupowner_id, submit_label).viewmodel
        
        return viewmodel

class GroupOwner_Details(Details_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, 
        poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)

        viewmodel = GroupOwner_Details(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel


class User_Delete(Delete_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, filter,
        poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolowner = PoolOwner.get_item_by_id(PoolOwner, poolowner_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelsuccess_bool, 
            poolowner, filter, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel
