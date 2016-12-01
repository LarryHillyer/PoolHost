from datetime import datetime

from django.db import models

from app.models import SiteUser, CronJobType
from app.mixins import HelperMixins

from cronjobtype.forms import CronJobTypeForm_Create, CronJobTypeForm_Edit

class BaseViewModel(object):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,
                            'modelsuccess_bool': modelsuccess_bool,
                            'modelstate': modelstate,
                            'modelstate_html': 'app/modelstatus.html' }

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtypes):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'cronjobtype-id' 

        self.viewmodel['create_url'] = 'cronjobtype:create'
        self.viewmodel['create_link_name'] = 'Create Cron Job Type'
        self.viewmodel['create_link_html'] = 'cronjobtype/create_link.html'

        self.viewmodel['index_table_html'] = 'cronjobtype/index_table.html'

        self.viewmodel['items'] = cronjobtypes 
        self.viewmodel['header_label_item'] = 'Cron Job Type Name'
        self.viewmodel['edit_url'] = 'cronjobtype:edit' 
        self.viewmodel['details_url'] = 'cronjobtype:details' 
        self.viewmodel['delete_url'] = 'cronjobtype:delete'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
        
        self.viewmodel['partial_view_id'] = 'cronjobtype-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_label_submit'] = submit_label

        self.viewmodel['index_url'] = 'cronjobtype:index'
        self.viewmodel['index_link_html'] = 'cronjobtype/index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class DescriptiveList_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'cronjobtype-id' 

        self.viewmodel['cronjobtype_id'] = cronjobtype.id

        self.viewmodel['descriptive_list'] = 'cronjobtype/descriptive_list.html' 

        self.viewmodel['item'] = cronjobtype 
        self.viewmodel['item_label_name'] = 'Cron Job Type'

        self.viewmodel['index_url'] = 'cronjobtype:index'


class Create_ViewModel(Form_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, submit_label)

        self.viewmodel['form_template_html'] = 'cronjobtype/create_form.html'  
        self.viewmodel['form_url'] = 'cronjobtype:create'
        self.viewmodel['form_html'] = 'cronjobtype/cronjobtype_form.html'

        self.viewmodel['form_label_name'] = 'Cron Job Type'

class Edit_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjobtype_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            submit_label)
        
        self.viewmodel['cronjobtype_id'] = cronjobtype_id

        self.viewmodel['form_template_html'] = 'cronjobtype/edit_form.html'
        self.viewmodel['form_html'] = 'cronjobtype/cronjobtype_form.html'
        self.viewmodel['form_url'] = 'cronjobtype:edit'

        self.viewmodel['form_label_name'] = 'Cron Type'

class Details_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)

        self.viewmodel['details_links_html'] = 'cronjobtype/details_links.html'

class Delete_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)

        self.viewmodel['delete_url'] = 'cronjobtype:delete'
        self.viewmodel['delete_form'] = 'cronjobtype/delete_form.html'


class SuperUser_Index(Index_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtypes):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtypes)

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)
        cronjobtypes = CronJobType.get_all_items(CronJobType)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, cronjobtypes).viewmodel

        return viewmodel

class SuperUser_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form, submit_label)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        form = CronJobTypeForm_Create()

        submit_label = 'Create'

        viewmodel = Create_ViewModel(site_user, title, modelstate, modelsuccess_bool, form, submit_label).viewmodel

        return viewmodel

class SuperUser_Edit(Edit_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjobtype_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            cronjobtype_id, submit_label)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, cronjobtype_id):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        cronjobtype = CronJobType.get_item_by_id(CronJobType, cronjobtype_id)
        
        form = CronJobTypeForm_Edit(instance = cronjobtype)

        submit_label = 'Edit'
        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            cronjobtype_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, cronjobtype_id):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        cronjobtype = CronJobType.get_item_by_id(CronJobType, cronjobtype_id)

        viewmodel = Details_ViewModel(site_user, title, modelstate, modelsuccess_bool, cronjobtype).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobtype):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobtype)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, cronjobtype_id):

        modelstate, modelsuccess_bool = CronJobType.get_modelstate(modelstate)

        cronjobtype = CronJobType.get_item_by_id(CronJobType, cronjobtype_id)

        viewmodel = Delete_ViewModel(site_user, title, modelstate, modelsuccess_bool, cronjobtype).viewmodel

        return viewmodel
