from datetime import datetime

from django.db import models

from app.models import SiteUser, CronJob, CronJobType, CronJobType_Choices
from app.mixins import HelperMixins

from cronjob.forms import CronJobForm_Create, CronJobForm_Edit


class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'cronjob-id'

        self.viewmodel['index_url'] = 'cronjob:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'cronjob:create'
        self.viewmodel['create_link_name'] = 'Create Cron Job'
        self.viewmodel['create_link_html'] =  'cronjob/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'cronjob/index_table.html' 

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'cronjob-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'cronjob/cronjob_form.html'

        self.viewmodel['form_label_name'] = 'Cron Job'
        self.viewmodel['form_label_cronjobtype'] = 'Cron Job Type'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'cronjob:index'
        self.viewmodel['index_link_html'] = 'cronjob/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            cronjob):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'cronjob-id' 

        self.viewmodel['cronjob_id'] = cronjob.id

        self.viewmodel['descriptive_list'] = 'cronjob/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'cronjob:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobs):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
      
        self.viewmodel['items'] = cronjobs 
        self.viewmodel['header_label_item'] = 'Cron Job'
        self.viewmodel['edit_url'] = 'cronjob:edit' 
        self.viewmodel['details_url'] = 'cronjob:details' 
        self.viewmodel['delete_url'] = 'cronjob:delete'

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            cronjob):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            cronjob)

        self.viewmodel['item'] = cronjob 
        self.viewmodel['item_label_name'] = 'Cron Job'
        self.viewmodel['item_label_cronjobtype'] = 'Cron Job Type'



class Create_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)

        self.viewmodel['form_template_html'] = 'cronjob/create_form.html' 
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html' 
        self.viewmodel['form_url'] = 'cronjob:create'

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjob_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)
        
        self.viewmodel['cronjob_id'] = cronjob_id

        self.viewmodel['form_template_html'] = 'cronjob/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_url'] = 'cronjob:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)

        self.viewmodel['edit_url'] = 'cronjob:edit'
        self.viewmodel['details_links_html'] = 'cronjob/details_links.html'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)

        self.viewmodel['delete_url'] = 'cronjob:delete'
        self.viewmodel['delete_form'] = 'cronjob/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjobs):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjobs)

        self.viewmodel['use_pagination'] = False            
        
    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)
        cronjobs = CronJob.get_all_items(CronJob)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, cronjobs).viewmodel

        return viewmodel

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, form):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)

        cronjobtypes = CronJobType.get_all_items(CronJobType)
        if cronjobtypes.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Cron Job Type First!'}
            return viewmodel

        cronjobtype_id = cronjobtypes[0].id
        CronJobType_Choices.get_cronjobtype_choices(cronjobtypes)

        if form == None:
            form = CronJobForm_Create(initial = {'cronjobtype_id':cronjobtype_id})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form).viewmodel

        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form,
        cronjob_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form,
            cronjob_id)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, cronjob_id, form):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)

        cronjob = CronJob.get_item_by_id(CronJob, cronjob_id)
        cronjobtypes = CronJobType.get_all_items(CronJobType)        
        CronJobType_Choices.get_cronjobtype_choices(cronjobtypes)

        if form == None:
            form = CronJobForm_Edit(instance = cronjob,  
                                    initial = {'cronjobtype_id':cronjob.cronjobtype_id})

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, 
            cronjob_id).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, cronjob_id):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)

        cronjob = CronJob.get_item_by_id(CronJob, cronjob_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, cronjob).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, cronjob):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, cronjob)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, cronjob_id):

        modelstate, modelsuccess_bool = CronJob.get_modelstate(modelstate)

        cronjob = CronJob.get_item_by_id(CronJob, cronjob_id)

        viewmodel = SuperUser_Delete(site_user, title, modelstate, modelsuccess_bool, cronjob).viewmodel

        return viewmodel
