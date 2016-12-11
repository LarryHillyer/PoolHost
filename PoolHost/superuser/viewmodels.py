from datetime import datetime

from django.db import models

from app.models import SiteUser, SuperUser
from app.mixins import HelperMixins

from superuser.forms import SuperUserForm_Create

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'superuser-id'

        self.viewmodel['index_url'] = 'superuser:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['create_url'] = 'superuser:create'
        self.viewmodel['create_link_name'] = 'Create Super User'
        self.viewmodel['create_link_html'] =  'superuser/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'

        self.viewmodel['index_table_html'] = 'superuser/index_table.html' 

        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'superuser-id' 

        self.viewmodel['form'] = form 
        self.viewmodel['form_html'] = 'superuser/superuser_form.html'

        self.viewmodel['form_label_name'] = 'Super User'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'superuser:index'
        self.viewmodel['index_link_html'] = 'superuser/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            superuser):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'superuser-id' 

        self.viewmodel['superuser_id'] = superuser.id

        self.viewmodel['descriptive_list'] = 'superuser/descriptive_list.html'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'superuser:index'


class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superusers):

        super().__init__(site_user, title, modelstate, modelsuccess_bool)
      
        self.viewmodel['items'] = superusers 
        self.viewmodel['header_label_item'] = 'Super User Name' 
        self.viewmodel['details_url'] = 'superuser:details' 
        self.viewmodel['delete_url'] = 'superuser:delete'

class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            superuser):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            superuser)

        self.viewmodel['item'] = superuser 
        self.viewmodel['item_label_name'] = 'Super User'
        self.viewmodel['item_label_email'] = 'E-mail'



class Create_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, form)

        self.viewmodel['form_template_html'] = 'superuser/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'   
        self.viewmodel['form_url'] = 'superuser:create'

        self.viewmodel['form_label_submit'] = 'Create'


class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)

        self.viewmodel['details_links_html'] = 'superuser/details_links.html'

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)

        self.viewmodel['delete_url'] = 'superuser:delete'
        self.viewmodel['delete_form'] = 'superuser/delete_form.html'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, superuser_id, modelstate):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        viewmodel = Delete_ViewModel(site_user, title, modelstate, modelsuccess_bool, superuser).viewmodel

        return viewmodel


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superusers):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superusers)

        self.viewmodel['use_pagination'] = False            

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)
        superusers = SuperUser.get_all_items(SuperUser)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, superusers).viewmodel

        return viewmodel

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        form):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            form)

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        form = SuperUserForm_Create()

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, 
            form).viewmodel

        return viewmodel

class SuperUser_Details(Details_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)
        
    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, superuser_id):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, superuser).viewmodel

        return viewmodel

class SuperUser_Delete(Delete_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, superuser):
        
        super().__init__(site_user, title, modelstate, modelsuccess_bool, superuser)

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, superuser_id):

        modelstate, modelsuccess_bool = SuperUser.get_modelstate(modelstate)

        superuser = SuperUser.get_item_by_id(SuperUser, superuser_id)

        viewmodel = SuperUser_Delete(site_user, title, modelstate, modelsuccess_bool, superuser).viewmodel

        return viewmodel
