from datetime import datetime

from django.db import models

from app.models import SiteUser, GroupOwner, GroupOwner_Choices
from app.mixins import HelperMixins

from groupowner.forms import GroupOwnerForm_Create, GroupOwnerForm_Transfer

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, filter):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'groupowner-id'

        self.viewmodel['filter' ] = filter

        self.viewmodel['index_url'] = 'groupowner:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'groupowner:create'
        self.viewmodel['create_link_name'] = 'Create Group Owner'
        self.viewmodel['create_link_html'] =  'groupowner/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'groupowner/index_table.html' 

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'groupowner-id' 

        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'groupowner/groupowner_form.html'

        self.viewmodel['form_label_name'] = 'Group Owner'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'groupowner:index'
        self.viewmodel['index_link_html'] = 'groupowner/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            groupowner, filter):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'groupowner-id' 

        self.viewmodel['groupowner_id'] = groupowner.id
        self.viewmodel['filter'] = filter

        self.viewmodel['descriptive_list'] = 'groupowner/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'groupowner:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, groupowners,
        filter):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, filter)
      
        self.viewmodel['items'] = groupowners 
        self.viewmodel['header_label_item'] = 'Group Owner'
        self.viewmodel['item_url'] = 'poolgroup:index'
        self.viewmodel['transfer_url'] = 'groupowner:transfer' 
        self.viewmodel['details_url'] = 'groupowner:details' 
        self.viewmodel['delete_url'] = 'groupowner:delete' 

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            groupowner, filter):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            groupowner, filter)

        self.viewmodel['item'] = groupowner 
        self.viewmodel['item_label_name'] = 'Group Owner'
        self.viewmodel['item_label_email'] = 'Group Owner E-Mail'

 
class Create_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            form, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form, filter)


        self.viewmodel['form_template_html'] = 'groupowner/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html' 
        self.viewmodel['form_url'] = 'groupowner:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Transfer_View(Form_Body_View):

    def __init__(self,site_user, title, modelstate, modelsuccess_bool, form, filter, groupowner):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter)

        self.viewmodel['groupowner_id'] = groupowner.id        

        self.viewmodel['form_template_html'] = 'groupowner/transfer_form.html'
        self.viewmodel['form_transfer_html'] = 'app/shared_transfer_form.html'  
        self.viewmodel['form_url'] = 'groupowner:transfer'
        self.viewmodel['form_html'] = 'groupowner/transfer_ownership_form.html'

        self.viewmodel['form_name'] = groupowner.name
        self.viewmodel['form_label_name'] = 'Existing Group Owner'
        self.viewmodel['form_label_new_groupowner'] = 'New Group Owner'

        self.viewmodel['form_label_submit'] = 'Transfer'

class Details_View(DescriptiveList_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, groupowner,  
        filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, groupowner,  
            filter)

        self.viewmodel['details_links_html'] = 'groupowner/details_links.html'
        self.viewmodel['transfer_url'] = 'groupowner:transfer'
       
class Delete_View(DescriptiveList_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, groupowner,  
        filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, groupowner,  
            filter)

        self.viewmodel['delete_url'] = 'groupowner:delete'
        self.viewmodel['delete_form'] = 'groupowner/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, groupowners, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, groupowners, filter)

        self.viewmodel['use_pagination'] = False           
        self.viewmodel['user_has_transfer_privileges'] = True
        

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter):

        modelstate, modelsuccess_bool = GroupOwner.get_modelstate(modelstate)

        groupowners = GroupOwner.get_all_items(GroupOwner)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, 
            groupowners, filter).viewmodel

        return viewmodel

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form, filter)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, filter, modelstate, form):

        modelstate, modelsuccess_bool = GroupOwner.get_modelstate(modelstate)

        if form == None:
            form = GroupOwnerForm_Create(initial = {'filter':filter})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, 
            form, filter).viewmodel

        return viewmodel

class SuperUser_Transfer(Transfer_View):

    def __init__(self,site_user, title, modelstate, modelsuccess_bool, form, filter, groupowner):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter, groupowner)

    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, groupowner_id, filter, modelstate, form):

        modelstate, modelsuccess_bool = GroupOwner.get_modelstate(modelstate)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)
        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)
        GroupOwner_Choices.get_different_choices_than_groupowner(groupowner_id, groupowners)
        groupowner_choices = GroupOwner_Choices.get_all_items(GroupOwner_Choices)

        if form == None:
            form = GroupOwnerForm_Transfer(initial = {'filter':filter,
                                                        'name': groupowner.name,
                                                        'new_groupowner_id': groupowner_choices[0].groupowner_id})

        viewmodel = SuperUser_Transfer(site_user, title, modelstate, modelsuccess_bool, 
            form, filter, groupowner).viewmodel

        return viewmodel

class SuperUser_Details(Details_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, groupowner,  
        filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, groupowner,  
            filter)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, groupowner_id, filter, modelstate):

        modelstate, modelsuccess_bool = GroupOwner.get_modelstate(modelstate)

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, groupowner,  
            filter).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, groupowner,  
        filter):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, groupowner,  
            filter)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, groupowner_id, filter, modelstate):

        modelstate, modelsuccess_bool = GroupOwner.get_modelstate(modelstate)

        groupowner = GroupOwner.get_item_by_id(GroupOwner, groupowner_id)

        viewmodel = SuperUser_Delete(site_user, title, modelstate, modelsuccess_bool, groupowner,  
            filter).viewmodel

        return viewmodel
