from datetime import datetime

from django.db import models

from app.models import SiteUser, CronJob, CronJobType, CronJobType_Choices
from app.mixins import HelperMixins

from cronjob.forms import CronJobForm_Create, CronJobForm_Edit

class BaseViewModel(object):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,
                            'modelsuccess_bool': modelsuccess_bool,
                            'modelstate': modelstate,
                            'modelstate_html': 'app/modelstatus.html' }

class Table_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobs):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'cronjob-id' 

        self.viewmodel['create_url'] = 'cronjob:create'
        self.viewmodel['create_link_name'] = 'Create Cron Job'
        self.viewmodel['create_link_html'] = 'cronjob/create_link.html'

        self.viewmodel['index_table_html'] = 'cronjob/index_table.html'

        self.viewmodel['items'] = cronjobs 
        self.viewmodel['header_label_item'] = 'Cron Job Name'
        self.viewmodel['edit_url'] = 'cronjob:edit' 
        self.viewmodel['details_url'] = 'cronjob:details' 
        self.viewmodel['delete_url'] = 'cronjob:delete'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
        
        self.viewmodel['partial_view_id'] = 'cronjob-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_label_submit'] = submit_label

        self.viewmodel['index_url'] = 'cronjob:index'
        self.viewmodel['index_link_html'] = 'cronjob/index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class DescriptiveList_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'cronjob-id' 

        self.viewmodel['cronjob_id'] = cronjob.id

        self.viewmodel['descriptive_list'] = 'cronjob/descriptive_list.html' 

        self.viewmodel['item'] = cronjob 
        self.viewmodel['item_label_name'] = 'Cron Job'
        self.viewmodel['item_label_cronjobtype'] = 'Cron Job Type'

        self.viewmodel['index_url'] = 'cronjob:index'


class Create_ViewModel(Form_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, submit_label)

        self.viewmodel['form_template_html'] = 'cronjob/create_form.html'  
        self.viewmodel['form_url'] = 'cronjob:create'
        self.viewmodel['form_html'] = 'cronjob/cronjob_form.html'

        self.viewmodel['form_label_name'] = 'Cron Job'
        self.viewmodel['form_label_cronjobtype'] = 'Cron Job Type'

class Edit_ViewModel(Form_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjob_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            submit_label)
        
        self.viewmodel['cronjob_id'] = cronjob_id

        self.viewmodel['form_template_html'] = 'cronjob/edit_form.html'
        self.viewmodel['form_html'] = 'cronjob/cronjob_form.html'
        self.viewmodel['form_url'] = 'cronjob:edit'

        self.viewmodel['form_label_name'] = 'Cron Job'
        self.viewmodel['form_label_cronjobtype'] = 'Cron Job Type'

class Details_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)

        self.viewmodel['details_links_html'] = 'cronjob/details_links.html'

class Delete_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)

        self.viewmodel['delete_url'] = 'cronjob:delete'
        self.viewmodel['delete_form'] = 'cronjob/delete_form.html'


class SuperUser_Index(Table_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobs):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobs)

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)
        cronjobs = CronJob.get_all_items(CronJob)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, cronjobs).viewmodel

        return viewmodel

class SuperUser_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form, submit_label)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)
        cronjobtypes = CronJobType.get_all_items(CronJobType)
        if cronjobtypes.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel

        cronjobtype_id = cronjobtypes[0].id
        CronJobType_Choices.get_cronjobtype_choices()

        form = CronJobForm_Create(initial = {'conjobtype_id':cronjobtype_id})

        submit_label = 'Create'

        viewmodel = Create_ViewModel(site_user, title, modelstate, modelsuccess_bool, form, submit_label).viewmodel

        return viewmodel

class SuperUser_Edit(Edit_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjob_id, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            cronjob_id, submit_label)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, cronjob_id):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)

        cronjob = CronJob.get_item_by_id(CronJob, cronjob_id)
        CronJobType_Choices.get_cronjobtype_choices()

        form = CronJobForm_Edit(instance = cronjob, initial = {'cronjobtype_id':cronjob.cronjobtype_id})

        submit_label = 'Edit'
        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            cronjob_id, submit_label).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, cronjob_id):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)

        cronjob = CronJob.get_item_by_id(CronJob, cronjob_id)

        viewmodel = Details_ViewModel(site_user, title, modelstate, modelsuccess_bool, cronjob).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, cronjob_id):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)

        cronjob = CronJob.get_item_by_id(CronJob, cronjob_id)

        viewmodel = Delete_ViewModel(site_user, title, modelstate, modelsuccess_bool, cronjob).viewmodel

        return viewmodel
