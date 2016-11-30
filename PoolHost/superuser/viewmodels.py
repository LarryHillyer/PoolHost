from datetime import datetime

from django.db import models

from app.models import SiteUser, SuperUser
from app.mixins import HelperMixins

from superuser.forms import SuperUserForm_Create

class BaseViewModel(object):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,
                            'modelsuccess_bool': modelsuccess_bool,
                            'modelstate': modelstate,
                            'modelstate_html': 'app/modelstatus.html' }

class Index_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superusers):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'superuser-id' # app/shared_index.html params

        self.viewmodel['create_url'] = 'superuser:create'
        self.viewmodel['create_link_name'] = 'Create Super User'
        self.viewmodel['create_link_html'] = 'superuser/create_link.html'

        self.viewmodel['index_table_html'] = 'superuser/index_table.html'

        self.viewmodel['items'] = superusers # super_user/index_table.html params
        self.viewmodel['header_label_item'] = 'Super User Name' 
        self.viewmodel['details_url'] = 'superuser:details' 
        self.viewmodel['delete_url'] = 'superuser:delete'

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
        
        self.viewmodel['partial_view_id'] = 'superuser-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_label_submit'] = submit_label

        self.viewmodel['index_url'] = 'superuser:index'
        self.viewmodel['index_link_html'] = 'superuser/index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class DescriptiveList_ViewModel(BaseViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)

        self.viewmodel['partial_view_id'] = 'superuser-id' 

        self.viewmodel['superuser_id'] = superuser.id

        self.viewmodel['descriptive_list'] = 'superuser/descriptive_list.html' 

        self.viewmodel['item'] = superuser 
        self.viewmodel['item_label_name'] = 'Super User'
        self.viewmodel['item_label_email'] = 'E-mail'

        self.viewmodel['index_url'] = 'superuser:index'


class Create_ViewModel(Form_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, submit_label)

        self.viewmodel['form_template_html'] = 'superuser/create_form.html'  
        self.viewmodel['form_url'] = 'superuser:create'
        self.viewmodel['form_html'] = 'superuser/superuser_form.html'

        self.viewmodel['form_label_name'] = 'Super User Name'

class Details_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)

        self.viewmodel['details_links_html'] = 'superuser/details_links.html'

class Delete_ViewModel(DescriptiveList_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)

        self.viewmodel['delete_url'] = 'superuser:delete'
        self.viewmodel['delete_form'] = 'superuser/delete_form.html'

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, superuser_id, modelstate):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        viewmodel = Delete_ViewModel(site_user, title, modelstate, modelsuccess_bool, superuser).viewmodel

        return viewmodel


class SuperUser_Index(Index_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superusers):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superusers)

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)
        superusers = SuperUser.get_all_items(SuperUser)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, superusers).viewmodel

        return viewmodel

class SuperUser_Create(Create_ViewModel):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form, submit_label):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form, submit_label)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        form = SuperUserForm_Create()

        submit_label = 'Create'

        viewmodel = Create_ViewModel(site_user, title, modelstate, modelsuccess_bool, form, submit_label).viewmodel

        return viewmodel

class SuperUser_Details(Details_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, superuser_id):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        viewmodel = Details_ViewModel(site_user, title, modelstate, modelsuccess_bool, superuser).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_ViewModel):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, superuser_id):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        viewmodel = Delete_ViewModel(site_user, title, modelstate, modelsuccess_bool, superuser).viewmodel

        return viewmodel
