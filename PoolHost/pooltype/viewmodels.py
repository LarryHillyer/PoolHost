from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolType
from app.mixins import HelperMixins

from pooltype.forms import PoolTypeForm_Create, PoolTypeForm_Edit


class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'pooltype-id'

        self.viewmodel['index_url'] = 'pooltype:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'pooltype:create'
        self.viewmodel['create_link_name'] = 'Create Pool Type'
        self.viewmodel['create_link_html'] =  'pooltype/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'pooltype/index_table.html' 

        self.viewmodel['home_url'] = 'home'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'pooltype-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'pooltype/pooltype_form.html'

        self.viewmodel['form_label_name'] = 'Pool Type'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'pooltype:index'
        self.viewmodel['index_link_html'] = 'pooltype/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pooltype):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'pooltype-id' 

        self.viewmodel['pooltype_id'] = pooltype.id

        self.viewmodel['descriptive_list'] = 'pooltype/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'pooltype:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltypes):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
      
        self.viewmodel['items'] = pooltypes 
        self.viewmodel['header_label_item'] = 'Pool Type'
        self.viewmodel['edit_url'] = 'pooltype:edit' 
        self.viewmodel['details_url'] = 'pooltype:details' 
        self.viewmodel['delete_url'] = 'pooltype:delete'

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pooltype):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pooltype)

        self.viewmodel['item'] = pooltype 
        self.viewmodel['item_label_name'] = 'Pool Type'


class Create_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)

        self.viewmodel['form_template_html'] = 'pooltype/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'  
        self.viewmodel['form_url'] = 'pooltype:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        pooltype_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form )
        
        self.viewmodel['pooltype_id'] = pooltype_id

        self.viewmodel['form_template_html'] = 'pooltype/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_url'] = 'pooltype:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)

        self.viewmodel['edit_url'] = 'pooltype:edit'
        self.viewmodel['details_links_html'] = 'pooltype/details_links.html'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)

        self.viewmodel['delete_url'] = 'pooltype:delete'
        self.viewmodel['delete_form'] = 'pooltype/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltypes):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltypes)

        self.viewmodel['use_pagination'] = False            

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)
        pooltypes = PoolType.get_all_items(PoolType)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, 
            pooltypes).viewmodel

        return viewmodel

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, form):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        if form == None:
            form = PoolTypeForm_Create()

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form).viewmodel

        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        pooltype_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            pooltype_id)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, pooltype_id, form):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        pooltype = PoolType.get_item_by_id(PoolType, pooltype_id)

        if form == None:        
            form = PoolTypeForm_Edit(instance = pooltype)

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            pooltype_id).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, pooltype_id):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        pooltype = PoolType.get_item_by_id(PoolType, pooltype_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, pooltype).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pooltype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, pooltype)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, pooltype_id):

        modelstate, modelsuccess_bool = PoolType.get_modelstate(modelstate)

        pooltype = PoolType.get_item_by_id(PoolType, pooltype_id)

        viewmodel = SuperUser_Delete(site_user, title, modelstate, modelsuccess_bool, pooltype).viewmodel

        return viewmodel
