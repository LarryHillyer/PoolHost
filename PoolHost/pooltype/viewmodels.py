from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolType
from app.mixins import HelperMixins

from pooltype.forms import PoolTypeForm_Create, PoolTypeForm_Edit

class BaseViewModel(object):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,
                            'modelsuccess_bool': modelsuccess_bool,
                            'modelstate': modelstate,
                            'modelstate_html': 'app/modelstatus.html' }

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltypes):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'pooltype-id' 

        self.viewmodel['create_url'] = 'pooltype:create'
        self.viewmodel['create_link_name'] = 'Create Pool Type'
        self.viewmodel['create_link_html'] = 'pooltype/create_link.html'

        self.viewmodel['index_table_html'] = 'pooltype/index_table.html'

        self.viewmodel['items'] = pooltypes 
        self.viewmodel['header_label_item'] = 'Pool Type Name'
        self.viewmodel['edit_url'] = 'pooltype:edit' 
        self.viewmodel['details_url'] = 'pooltype:details' 
        self.viewmodel['delete_url'] = 'pooltype:delete'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
        
        self.viewmodel['partial_view_id'] = 'pooltype-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_label_submit'] = submit_label

        self.viewmodel['index_url'] = 'pooltype:index'
        self.viewmodel['index_link_html'] = 'pooltype/index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class DescriptiveList_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'pooltype-id' 

        self.viewmodel['pooltype_id'] = pooltype.id

        self.viewmodel['descriptive_list'] = 'pooltype/descriptive_list.html' 

        self.viewmodel['item'] = pooltype 
        self.viewmodel['item_label_name'] = 'Pool Type'

        self.viewmodel['index_url'] = 'pooltype:index'


class Create_ViewModel(Form_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, submit_label)

        self.viewmodel['form_template_html'] = 'pooltype/create_form.html'  
        self.viewmodel['form_url'] = 'pooltype:create'
        self.viewmodel['form_html'] = 'pooltype/pooltype_form.html'

        self.viewmodel['form_label_name'] = 'Pool Type'

class Edit_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        pooltype_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            submit_label)
        
        self.viewmodel['pooltype_id'] = pooltype_id

        self.viewmodel['form_template_html'] = 'pooltype/edit_form.html'
        self.viewmodel['form_html'] = 'pooltype/pooltype_form.html'
        self.viewmodel['form_url'] = 'pooltype:edit'

        self.viewmodel['form_label_name'] = 'Pool Type'


class Details_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)

        self.viewmodel['details_links_html'] = 'pooltype/details_links.html'

class Delete_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)

        self.viewmodel['delete_url'] = 'pooltype:delete'
        self.viewmodel['delete_form'] = 'pooltype/delete_form.html'


class SuperUser_Index(Index_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltypes):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltypes)

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)
        pooltypes = PoolType.get_all_items(PoolType)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, pooltypes).viewmodel

        return viewmodel

class SuperUser_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form, submit_label)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        form = PoolTypeForm_Create()

        submit_label = 'Create'

        viewmodel = Create_ViewModel(site_user, title, modelstate, modelsuccess_bool, form, submit_label).viewmodel

        return viewmodel

class SuperUser_Edit(Edit_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        pooltype_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            pooltype_id, submit_label)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, pooltype_id):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        pooltype = PoolType.get_item_by_id(PoolType, pooltype_id)
        
        form = PoolTypeForm_Edit(instance = pooltype)

        submit_label = 'Edit'
        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            pooltype_id, submit_label).viewmodel
        
        return viewmodel


class SuperUser_Details(Details_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, pooltype_id):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        pooltype = PoolType.get_item_by_id(PoolType, pooltype_id)

        viewmodel = Details_ViewModel(site_user, title, modelstate, modelsuccess_bool, pooltype).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, pooltype_id):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        pooltype = PoolType.get_item_by_id(PoolType, pooltype_id)

        viewmodel = Delete_ViewModel(site_user, title, modelstate, modelsuccess_bool, pooltype).viewmodel

        return viewmodel
