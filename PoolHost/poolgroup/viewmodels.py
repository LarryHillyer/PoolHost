from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolGroup, GroupOwner, SuperUser, GroupOwner_Choices, PoolGroup_Choices
from app.mixins import HelperMixins

from poolgroup.forms import PoolGroupForm_Create, PoolGroupForm_Edit, PoolGroupForm_Transfer

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, groupowners, 
        filter, groupowner_id):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'poolgroup-id'

        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter' ] = filter

        self.viewmodel['index_url'] = 'poolgroup:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['superuser_pagination_list_html'] = 'poolgroup/superuser_pagination_list.html' 
        self.viewmodel['groupowner_pagination_list_html'] = 'poolgroup/groupowner_pagination_list.html'

        self.viewmodel['shared_groupowner_pagination_list_html'] = 'app/shared_groupowner_pagination_list.html'
        self.viewmodel['shared_poolgroup_pagination_list_html'] = 'app/shared_poolgroup_pagination_list.html'
        self.viewmodel['shared_poolowner_pagination_list_html'] = 'app/shared_poolowner_pagination_list.html'

        self.viewmodel['groupowner_pagination_link_html'] = 'poolgroup/groupowner_pagination_link.html'
        self.viewmodel['poolgroup_pagination_link_html'] = 'poolgroup/poolgroup_pagination_link.html'
        self.viewmodel['poolowner_pagination_link_html'] = 'poolgroup/poolowner_pagination_link.html'
                           
        self.viewmodel['groupowners'] = groupowners

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'poolgroup:create'
        self.viewmodel['create_link_name'] = 'Create Pool Group'
        self.viewmodel['create_link_html'] =  'poolgroup/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'poolgroup/index_table.html' 

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'poolgroup-id' 

        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'poolgroup/poolgroup_form.html'

        self.viewmodel['form_label_name'] = 'Pool Group'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'poolgroup:index'
        self.viewmodel['index_link_html'] = 'poolgroup/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolgroup, filter, groupowner_id):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'poolgroup-id' 

        self.viewmodel['poolgroup_id'] = poolgroup.id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['descriptive_list'] = 'poolgroup/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'poolgroup:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroups,   
        groupowners, filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, groupowners, 
            filter, groupowner_id)
      
        self.viewmodel['items'] = poolgroups 
        self.viewmodel['header_label_item'] = 'Pool Group'
        self.viewmodel['header_label_groupowner'] = 'Group Owner' 
        self.viewmodel['item_url'] = 'poolowner:index'
        self.viewmodel['transfer_url'] = 'poolgroup:transfer' 
        self.viewmodel['edit_url'] = 'poolgroup:edit'
        self.viewmodel['details_url'] = 'poolgroup:details' 
        self.viewmodel['delete_url'] = 'poolgroup:delete' 

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            poolgroup, filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            poolgroup, filter, groupowner_id)

        self.viewmodel['item'] = poolgroup 
        self.viewmodel['item_label_name'] = 'Pool Group'
        self.viewmodel['item_label_groupowner_name'] = 'Group Owner'

                       
class Create_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id)
        
        self.viewmodel['form_template_html'] = 'poolgroup/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'
        self.viewmodel['form_url'] = 'poolgroup:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id)
        
        self.viewmodel['poolgroup_id'] = poolgroup_id

        self.viewmodel['form_template_html'] = 'poolgroup/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_url'] = 'poolgroup:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Transfer_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool,  form,
         filter, poolgroup, groupowner_id):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, 
            filter, groupowner_id)

        self.viewmodel['poolgroup_id'] = poolgroup.id

        self.viewmodel['form_template_html'] = 'poolgroup/transfer_form.html'
        self.viewmodel['form_transfer_html'] = 'app/shared_transfer_form.html' 
        self.viewmodel['form_url'] = 'poolgroup:transfer'
        self.viewmodel['form_html'] = 'poolgroup/transfer_ownership_form.html'

        self.viewmodel['form_name'] = poolgroup.name
        self.viewmodel['form_label_name'] = 'Pool Group'
        self.viewmodel['form_label_groupowner'] = 'Existing Group Owner'
        self.viewmodel['form_groupowner_name'] = poolgroup.groupowner.name
        self.viewmodel['form_label_new_groupowner'] = 'New Group Owner'

        self.viewmodel['form_label_submit'] = 'Transfer'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id)

        self.viewmodel['edit_url'] = 'poolgroup:edit'
        self.viewmodel['transfer_url'] = 'poolgroup:transfer'
        self.viewmodel['details_links_html'] = 'poolgroup/details_links.html'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup,  
        filter, groupowner_id)

        self.viewmodel['delete_url'] = 'poolgroup:delete'
        self.viewmodel['delete_form'] = 'poolgroup/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter, 
            groupowner_id) 

        self.viewmodel['use_pagination'] = True            

        self.viewmodel['user_has_transfer_privileges'] = True

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

            groupowners = GroupOwner.get_all_items(GroupOwner)

            if groupowners.count() == 0:
                poolgroups = []               
                return groupowner_id, poolgroups

            if groupowner_id == 0:
                groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)       
               
            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        return groupowner_id, poolgroups

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id)
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id, form):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)
        GroupOwner_Choices.get_choices_by_groupowners(groupowners)

        if form == None:
            form = PoolGroupForm_Create(initial={'groupowner_id' : groupowner_id,
                                                        'filter' : filter})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            groupowner_id).viewmodel
        
        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolgroup_id, groupowner_id)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        groupowner_id = poolgroup.groupowner_id
        groupowners = GroupOwner.get_all_items(GroupOwner)
        GroupOwner_Choices.get_choices_by_groupowners(groupowners)
        
        if form == None:       
            form = PoolGroupForm_Edit(initial = {'id': poolgroup.id,
                                                 'name': poolgroup.name,
                                                 'groupowner_id': poolgroup.groupowner_id,
                                                 'filter':filter})

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class SuperUser_Transfer(Transfer_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolgroup, groupowner_id):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,  filter,
            poolgroup, groupowner_id)

    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id, 
            form):

        modelstate, modelsuccess_bool = GroupOwner.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)
        
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, poolgroup.groupowner_id)

        GroupOwner_Choices.get_different_choices_than_groupowner(groupowner_id, groupowners)
        groupowner_choices = GroupOwner_Choices.get_all_items(GroupOwner_Choices)

        if form == None:
            form = PoolGroupForm_Transfer(initial = {'filter':filter,
                                                        'name': poolgroup.name,
                                                        'groupowner_name': poolgroup.groupowner.name,
                                                        'new_groupowner_id': groupowner_choices[0].groupowner_id})

        viewmodel = SuperUser_Transfer(site_user, title, modelstate, modelsuccess_bool, form,  filter, poolgroup, 
            groupowner_id).viewmodel

        return viewmodel

class SuperUser_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup, 
        filter, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup, 
            filter, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, 
        groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)
        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, 
            poolgroup, filter, groupowner_id).viewmodel
        
        return viewmodel


class GroupOwner_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter,
            groupowner_id) 

        self.viewmodel['use_pagination'] = False           
        self.viewmodel['user_has_transfer_privileges'] = False

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter = None):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id
        groupowners = GroupOwner.get_items_by_id(GroupOwner, groupowner_id)

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        viewmodel = GroupOwner_Index(site_user, title, modelstate, modelsuccess_bool, poolgroups, groupowners, filter, groupowner_id).viewmodel
        
        return viewmodel
       
class GroupOwner_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            groupowner_id) 

        self.viewmodel['form_url'] = 'poolgroup:create'

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, groupowner_id, form):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        if form == None:
            form = PoolGroupForm_Create(initial = {'groupowner_id' : groupowner_id,
                                                               'filter': filter})

        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        viewmodel = GroupOwner_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            groupowner_id).viewmodel
        
        return viewmodel

class GroupOwner_Edit(Edit_View):

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

class GroupOwner_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
            groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = GroupOwner_Details(site_user, title, modelstate, modelsuccess_bool, 
            poolgroup, filter, groupowner_id).viewmodel
        
        return viewmodel


class User_Delete(Delete_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
        groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolgroup, filter,
            groupowner_id) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, filter, poolgroup_id,
        groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolgroup = PoolGroup.get_item_by_id(PoolGroup, poolgroup_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelsuccess_bool, poolgroup, 
            filter, groupowner_id).viewmodel
        
        return viewmodel
