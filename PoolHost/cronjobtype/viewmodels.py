from datetime import datetime

from django.db import models

from app.models import SiteUser, CronJobType
from app.mixins import HelperMixins

from cronjobtype.forms import CronJobTypeForm_Create, CronJobTypeForm_Edit

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'cronjobtype-id'

        self.viewmodel['index_url'] = 'cronjobtype:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'cronjobtype:create'
        self.viewmodel['create_link_name'] = 'Create Cron Job Type'
        self.viewmodel['create_link_html'] =  'cronjobtype/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'cronjobtype/index_table.html' 

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'cronjobtype-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'cronjobtype/cronjobtype_form.html'

        self.viewmodel['form_label_name'] = 'Cron Job Type'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'cronjobtype:index'
        self.viewmodel['index_link_html'] = 'cronjobtype/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            cronjobtype):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'cronjobtype-id' 

        self.viewmodel['cronjobtype_id'] = cronjobtype.id

        self.viewmodel['descriptive_list'] = 'cronjobtype/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'cronjobtype:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtypes):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
      
        self.viewmodel['items'] = cronjobtypes 
        self.viewmodel['header_label_item'] = 'Cron Job Type'
        self.viewmodel['edit_url'] = 'cronjobtype:edit' 
        self.viewmodel['details_url'] = 'cronjobtype:details' 
        self.viewmodel['delete_url'] = 'cronjobtype:delete'

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            cronjobtype):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            cronjobtype)

        self.viewmodel['item'] = cronjobtype 
        self.viewmodel['item_label_name'] = 'Cron Job Type'


class Create_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)

        self.viewmodel['form_template_html'] = 'cronjobtype/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'  
        self.viewmodel['form_url'] = 'cronjobtype:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjobtype_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)
        
        self.viewmodel['cronjobtype_id'] = cronjobtype_id

        self.viewmodel['form_template_html'] = 'cronjobtype/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_url'] = 'cronjobtype:edit'

        self.viewmodel['form_label_submit'] = 'Create'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)

        self.viewmodel['edit_url'] = 'cronjobtype:edit'
        self.viewmodel['details_links_html'] = 'cronjobtype/details_links.html'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)

        self.viewmodel['delete_url'] = 'cronjobtype:delete'
        self.viewmodel['delete_form'] = 'cronjobtype/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtypes):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtypes)

        self.viewmodel['use_pagination'] = False            

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)
        cronjobtypes = CronJobType.get_all_items(CronJobType)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, cronjobtypes).viewmodel

        return viewmodel

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        form = CronJobTypeForm_Create()

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form).viewmodel

        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjobtype_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            cronjobtype_id)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, cronjobtype_id):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        cronjobtype = CronJobType.get_item_by_id(CronJobType, cronjobtype_id)
        
        form = CronJobTypeForm_Edit(instance = cronjobtype)

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            cronjobtype_id).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, cronjobtype_id):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        cronjobtype = CronJobType.get_item_by_id(CronJobType, cronjobtype_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, cronjobtype).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, cronjobtype_id):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        cronjobtype = CronJobType.get_item_by_id(CronJobType, cronjobtype_id)

        viewmodel = SuperUser_Delete(site_user, title, modelstate, modelsuccess_bool, cronjobtype).viewmodel

        return viewmodel
