from datetime import datetime

from django.db import models

from app.models import SiteUser, Pool, PoolOwner, PoolGroup, GroupOwner, SuperUser 
from app.models import GroupOwner_Choices, PoolGroup_Choices, PoolOwner_Choices
from app.models import CronJob, CronJob_Choices, PoolType, PoolType_Choices
from app.mixins import HelperMixins

from pool.forms import PoolForm_Create, PoolForm_Edit, PoolForm_Transfer

class Layout_View(object):

    def __init__(self, site_user, title):

        self.viewmodel = {'site_user':site_user, # app/layout.html params
                            'title': title,
                            'year': datetime.now().year,}

class Index_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, poolowners, 
        poolgroups, groupowners, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title)

        self.viewmodel['partial_view_id'] = 'pool-id'

        self.viewmodel['poolowner_id'] = poolowner_id
        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter' ] = filter

        self.viewmodel['index_url'] = 'pool:index'

        self.viewmodel['pagination_routing_html'] = 'app/pagination_routing.html'  

        self.viewmodel['superuser_pagination_list_html'] = 'pool/superuser_pagination_list.html' 
        self.viewmodel['groupowner_pagination_list_html'] = 'pool/groupowner_pagination_list.html'

        self.viewmodel['shared_groupowner_pagination_list_html'] = 'app/shared_groupowner_pagination_list.html'
        self.viewmodel['shared_poolgroup_pagination_list_html'] = 'app/shared_poolgroup_pagination_list.html'
        self.viewmodel['shared_poolowner_pagination_list_html'] = 'app/shared_poolowner_pagination_list.html'

        self.viewmodel['groupowner_pagination_link_html'] = 'pool/groupowner_pagination_link.html'
        self.viewmodel['poolgroup_pagination_link_html'] = 'pool/poolgroup_pagination_link.html'
        self.viewmodel['poolowner_pagination_link_html'] = 'pool/poolowner_pagination_link.html'

        self.viewmodel['poolowners'] = poolowners                             
        self.viewmodel['poolgroups'] = poolgroups 
        self.viewmodel['groupowners'] = groupowners

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_table_html'] = 'pool/index_table.html' 

        self.viewmodel['create_url'] = 'pool:create'
        self.viewmodel['create_link_name'] = 'Create Pool'
        self.viewmodel['create_link_html'] =  'pool/create_link.html' 
        self.viewmodel['shared_create_link_html'] = 'app/shared_create_link.html'
 
        self.viewmodel['scripts'] = ['app/scripts/Client/TableStripping.js']

class Form_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title)
        
        self.viewmodel['partial_view_id'] = 'pool-id' 

        self.viewmodel['poolowner_id'] = poolowner_id
        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['form'] = form
        self.viewmodel['form_html'] = 'pool/pool_form.html'

        self.viewmodel['form_label_name'] = 'Pool'
        self.viewmodel['form_label_cronjob'] = 'Cron Job'
        self.viewmodel['form_label_pooltype'] = 'Pool Type'
        self.viewmodel['form_label_groupowner'] = 'Group Owner'
        self.viewmodel['form_label_poolgroup'] = 'Pool Group'
        self.viewmodel['form_label_poolowner'] = 'Pool Owner'

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['index_url'] = 'pool:index'
        self.viewmodel['index_link_html'] = 'pool/index_link.html'
        self.viewmodel['shared_index_link_html'] = 'app/shared_index_link.html'

        self.viewmodel['scripts'] = ['app/scripts/jquery.validate.js', 'app/scripts/Client/GOwner_PGroup_POwner_CDD.js']

class Details_Delete_Body_View(Layout_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title)


        self.viewmodel['partial_view_id'] = 'superuser-id' 

        self.viewmodel['pool_id'] = pool.id
        self.viewmodel['poolowner_id'] = poolowner_id
        self.viewmodel['poolgroup_id'] = poolgroup_id
        self.viewmodel['groupowner_id'] = groupowner_id
        self.viewmodel['filter'] = filter

        self.viewmodel['modelsuccess_bool'] = modelsuccess_bool
        self.viewmodel['modelstate'] = modelstate
        self.viewmodel['modelstate_html'] = 'app/modelstatus.html'

        self.viewmodel['descriptive_list'] = 'pool/descriptive_list.html' 

        self.viewmodel['index_url'] = 'pool:index'

               
class Table_View(Index_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pools, poolowners, 
        poolgroups, groupowners, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, poolowners, 
            poolgroups, groupowners, filter, poolowner_id, poolgroup_id, groupowner_id)
     
 
        self.viewmodel['items'] = pools # pool/index_table.html params
        self.viewmodel['header_label_item'] = 'Pool'
        self.viewmodel['header_label_groupowner'] = 'Group Owner'
        self.viewmodel['header_label_cronjob'] = 'CronJob'
        self.viewmodel['header_label_poolowner'] = 'Pool Owner'
        self.viewmodel['header_label_poolgroup'] = 'Pool Group'
        self.viewmodel['item_url'] = 'pool:index'
        self.viewmodel['transfer_url'] = 'pool:transfer'
        self.viewmodel['edit_url'] = 'pool:edit' 
        self.viewmodel['details_url'] = 'pool:details' 
        self.viewmodel['delete_url'] = 'pool:delete' 
                        
class DescriptiveList_View(Details_Delete_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
        pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id)


        self.viewmodel['item'] = pool 
        self.viewmodel['item_label_name'] = 'Pool'
        self.viewmodel['item_label_poolowner'] = 'Pool Owner'
        self.viewmodel['item_label_cronjob'] = 'Cron Job'
        self.viewmodel['item_label_pooltype'] = 'Pool Type'
        self.viewmodel['item_label_poolgroup'] = 'Pool Group'
        self.viewmodel['item_label_groupowner'] = 'Group Owner'


class Create_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolowner_id, poolgroup_id, groupowner_id)
 
        self.viewmodel['form_template_html'] = 'pool/create_form.html'
        self.viewmodel['form_create_html'] = 'app/shared_create_form.html'
        self.viewmodel['form_url'] = 'pool:create'       

        self.viewmodel['form_label_submit'] = 'Create'

class Edit_View(Form_Body_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        pool_id, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolowner_id, poolgroup_id, groupowner_id)
        
        self.viewmodel['pool_id'] = pool_id

        self.viewmodel['form_template_html'] = 'pool/edit_form.html'
        self.viewmodel['form_edit_html'] = 'app/shared_edit_form.html'
        self.viewmodel['form_url'] = 'pool:edit'

        self.viewmodel['form_label_submit'] = 'Edit'

class Transfer_View(Form_Body_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter, pool,
        poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolowner_id, poolgroup_id, groupowner_id)
        
        self.viewmodel['pool_id'] = pool.id

        self.viewmodel['form_template_html'] = 'pool/transfer_form.html'
        self.viewmodel['form_transfer_html'] = 'app/shared_transfer_form.html' 
        self.viewmodel['form_url'] = 'pool:transfer'
        self.viewmodel['form_html'] = 'pool/transfer_ownership_form.html'

        self.viewmodel['form_label_name'] = 'Existing Pool Owner'
        self.viewmodel['form_label_poolgroup'] = 'Pool Group'
        self.viewmodel['form_label_new_pool'] = 'New Pool Owner'

        self.viewmodel['form_label_submit'] = 'Transfer'

class Details_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id)

        self.viewmodel['details_links_html'] = 'pool/details_links.html'
        self.viewmodel['transfer_url'] = 'pool:transfer'
        self.viewmodel['edit_url'] = 'pool:edit' 

class Delete_View(DescriptiveList_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id)

        self.viewmodel['delete_form'] = 'pool/delete_form.html'
        self.viewmodel['delete_url'] = 'pool:delete'
        self.viewmodel['shared_delete_form_html'] = 'app/shared_delete_form.html'


class SuperUser_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pools, poolowners, poolgroups, groupowners, filter,
        poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, pools, poolowners, poolgroups, groupowners, filter,
            poolowner_id, poolgroup_id, groupowner_id) 

        self.viewmodel['use_pagination'] = True            
        self.viewmodel['user_has_transfer_privileges'] = True
       
    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, 
            poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id, poolgroup_id, poolowner_id, pools = SuperUser_Index.get_viewmodel_parameters_by_state(filter, poolowner_id, poolgroup_id, groupowner_id)
        
        groupowners = GroupOwner.get_all_items(GroupOwner)
        if groupowner_id == 0:
            poolgroups = PoolGroup.get_all_items(PoolGroup)
        else:
            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        if groupowner_id == 0 and poolgroup_id == 0 :
            poolowners = PoolOwner.get_all_items(PoolOwner)
            poolowners = PoolOwner.get_items_without_dups(PoolOwner,poolowners)
        elif groupowner_id != 0 and poolgroup_id == 0:
            poolowners = PoolOwner.get_items_by_groupowner_id(PoolOwner, groupowner_id)
            poolowners = PoolOwner.get_items_without_dups(PoolOwner,poolowners)
        else:
            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)

        viewmodel = SuperUser_Index(site_user, title, modelstate, modelsuccess_bool, 
            pools, poolowners, poolgroups, groupowners, filter, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

    @classmethod
    def get_viewmodel_parameters_by_state(cls,  filter, poolowner_id, poolgroup_id, groupowner_id):

        if filter == 0:

            groupowner_id = 0
            poolgroup_id = 0
            poolowner_id = 0
            pools = Pool.get_all_items(Pool)

        elif filter == 1:

            groupowners = GroupOwner.get_all_items(GroupOwner)

            if groupowners.count() == 0:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools

            if groupowner_id == 0:     
                groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)
                       
            groupowners = GroupOwner.get_items_by_id(GroupOwner, groupowner_id)

            pools = Pool.get_pools_by_groupowners(groupowners)

        elif filter == 2:

            poolgroups = PoolGroup.get_all_items(PoolGroup)

            if poolgroups.count() == 0:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools

            if poolgroup_id == 0:
                poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)
            poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)

            pools = Pool.get_pools_by_poolgroups(poolgroups)

        elif filter == 3:

            if groupowner_id == 0:
                groupowner_id = PoolGroup.get_item_by_id(PoolGroup,poolgroup_id).groupowner_id

            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

            if poolgroups.count() == 0:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools

            if poolgroup_id == 0:
                poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)
            poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)
            
            pools = Pool.get_pools_by_poolgroups(poolgroups)

        elif filter == 4:

            poolowners = PoolOwner.get_all_items(PoolOwner)

            if poolowners.count() == 0:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools
       
            if poolowner_id == 0:
                poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)

            poolowner_name = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).name
            poolowners = PoolOwner.get_items_by_name(PoolOwner, poolowner_name)

            pools = Pool.get_pools_by_poolowners(poolowners)
            pools = Pool.filter_pools(pools, groupowner_id, poolgroup_id, poolowner_id)

        elif filter == 5:

            if groupowner_id == 0:
                groupowner_id = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).poolgroup.groupowner_id                      

            poolowners = PoolOwner.get_items_by_groupowner_id(PoolOwner,groupowner_id)

            if poolowners == []:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools

            if poolowner_id == 0:
                poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)

            poolowner_name = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).name
            poolowners = PoolOwner.get_items_by_name(PoolOwner, poolowner_name)

            pools = Pool.get_pools_by_poolowners(poolowners)
            pools = Pool.filter_pools(pools, groupowner_id, poolgroup_id, poolowner_id)

        elif filter == 6:

            if poolgroup_id == 0:
                poolgroup_id = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).poolgroup_id                      

            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner,poolgroup_id)

            if poolowners.count() == 0:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools

            if poolowner_id == 0:
                poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)

            poolowner_name = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).name
            poolowners = PoolOwner.get_items_by_name(PoolOwner, poolowner_name)

            pools = Pool.get_pools_by_poolowners(poolowners)
            pools = Pool.filter_pools(pools, groupowner_id, poolgroup_id, poolowner_id)

        elif filter == 7:

            if groupowner_id == 0:
                groupowner_id = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).poolgroup.groupowner_id                      

            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

            if poolgroups.count() == 0:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools

            if poolgroup_id == 0:
                poolgroup_id = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).poolgroup_id

            poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)

            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)

            if poolowners.count() == 0:
                pools = []               
                return groupowner_id, poolgroup_id, poolowner_id, pools

            if poolowner_id == 0:
                poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)

            poolowner_name = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).name
            poolowners = PoolOwner.get_items_by_name(PoolOwner, poolowner_name)

            pools = Pool.get_pools_by_poolowners(poolowners)
            pools = Pool.filter_pools(pools, groupowner_id, poolgroup_id, poolowner_id)                            

        return groupowner_id, poolgroup_id, poolowner_id, pools

class SuperUser_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            poolowner_id, poolgroup_id, groupowner_id)
        
    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        groupowners = GroupOwner.get_groupowners_with_poolowners(groupowners)
        if len(groupowners) == 0:
            viewmodel = {'modelstate':'Error: Create a Group Owner First!'}
            return viewmodel
        GroupOwner_Choices.get_choices_by_groupowners(groupowners)

        groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        poolgroups = PoolGroup.get_poolgroups_with_poolowners(poolgroups)
        if len(poolgroups) == 0:
            viewmodel = {'modelstate':'Error: Create a Pool Group First!'}
            return viewmodel
        PoolGroup_Choices.get_choices_by_poolgroups(poolgroups)

        poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)

        poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        if poolowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Pool Owner First!'}
            return viewmodel
        
        poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)
        PoolOwner_Choices.get_choices_by_poolowners(poolowners)

        cronjobs = CronJob.get_all_items(CronJob)
        CronJob_Choices.get_cronjob_choices(cronjobs)
        cronjob_id = CronJob_Choices.get_all_items(CronJob_Choices)[0].cronjob_id

        pooltypes = PoolType.get_all_items(PoolType)
        PoolType_Choices.get_pooltype_choices(pooltypes)
        pooltype_id = PoolType_Choices.get_all_items(PoolType_Choices)[0].pooltype_id

        if form == None:        
            form = PoolForm_Create(initial = {'cronjob_id': cronjob_id,
                                            'pooltype_id': pooltype_id,
                                            'groupowner_id': groupowner_id,
                                            'poolgroup_id': poolgroup_id,
                                            'poolowner_id' : poolowner_id,
                                            'filter' : filter})

        viewmodel = SuperUser_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class SuperUser_Edit(Edit_View):
    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        pool_id, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            pool_id, poolowner_id, poolgroup_id, groupowner_id)


    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, filter, pool_id, poolowner_id, 
        poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = Pool.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        groupowners = GroupOwner.get_groupowners_with_poolowners(groupowners)
        GroupOwner_Choices.get_choices_by_groupowners(groupowners)

        groupowner_id = pool.poolgroup.groupowner_id

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        poolgroups = PoolGroup.get_poolgroups_with_poolowners(poolgroups)
        PoolGroup_Choices.get_choices_by_poolgroups(poolgroups)

        poolgroup_id = pool.poolgroup_id

        poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        PoolOwner_Choices.get_choices_by_poolowners(poolowners)

        poolowner_id = pool.poolowner_id

        cronjobs = CronJob.get_all_items(CronJob)
        CronJob_Choices.get_cronjob_choices(cronjobs)
        cronjob_id = pool.cronjob_id

        pooltypes = PoolType.get_all_items(PoolType)
        PoolType_Choices.get_pooltype_choices(pooltypes)
        pooltype_id = pool.pooltype_id

        if form == None:        
            form = PoolForm_Edit(initial = {'id': pool_id,
                                                'name': pool.name,
                                                'cronjob_id': cronjob_id,
                                                'pooltype_id': pooltype_id,
                                                'groupowner_id': groupowner_id,
                                                'poolgroup_id': poolgroup_id,
                                                'poolowner_id' : poolowner_id,
                                                'filter' : filter})

        viewmodel = SuperUser_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            pool_id, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class SuperUser_Transfer(Transfer_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        pool, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            pool, poolowner_id, poolgroup_id, groupowner_id)
        
    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, modelstate, filter, pool_id, poolowner_id, 
        poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = Pool.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, pool.poolgroup_id)
        PoolOwner_Choices.get_different_choices_than_poolowner(pool.poolowner_id, poolowners)
        poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
        if poolowner_choices.count() == 0:
            viewmodel = {'modelstate':'Error: No other poolowner is in pool group, add a pool owner to pool group first!'}
            return viewmodel

        if form == None:
            form = PoolForm_Transfer(initial={'name' : pool.name,
                                                'new_poolowner_id': poolowner_choices[0].poolowner_id,
                                                'poolgroup_name': pool.poolgroup.name,
                                                'filter' : filter})

        viewmodel = SuperUser_Transfer(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            pool, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class SuperUser_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, pool_id, 
        poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        viewmodel = SuperUser_Details(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel


class GroupOwner_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pools, poolowners, poolgroups, groupowners, 
        filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, pools, poolowners, poolgroups, groupowners, 
            filter, poolowner_id, poolgroup_id, groupowner_id) 

        self.viewmodel['use_pagination'] = True  # app/shared_index_pagination.html          
        self.viewmodel['user_has_transfer_privileges'] = True

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id

        poolgroup_id, poolowner_id, pools = GroupOwner_Index.get_viewmodel_parameters_by_state(filter, poolowner_id, 
            poolgroup_id, groupowner_id)

        groupowners = [GroupOwner.get_item_by_id(GroupOwner,groupowner_id)]

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        if poolgroup_id == 0:
            poolowners = PoolOwner.get_items_by_groupowner_id(PoolOwner, groupowner_id)
            poolowners = PoolOwner.get_items_without_dups(PoolOwner,poolowners)
        else:
            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)       

        viewmodel = GroupOwner_Index(site_user, title, modelstate, modelsuccess_bool, pools, poolowners, 
            poolgroups, groupowners, filter, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

    @classmethod
    def get_viewmodel_parameters_by_state(cls,  filter, poolowner_id, poolgroup_id, groupowner_id):

        if filter == 0:

            poolgroup_id = 0
            poolowner_id = 0

            pools = Pool.get_items_by_groupowner_id(Pool, groupowner_id)

        elif filter == 1:

            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

            if poolgroups.count() == 0:
                pools = []               
                return poolgroup_id, poolowner_id, pools

            if poolgroup_id == 0:
                poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)
            poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)

            pools = Pool.get_pools_by_poolgroups(poolgroups)            


        elif filter == 2:

            poolowners = PoolOwner.get_items_by_groupowner_id(PoolOwner, groupowner_id)

            if poolowners == []:
                pools = []               
                return poolgroup_id, poolowner_id, pools

            if poolowner_id == 0:
                poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)

            poolowner_name = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).name
            poolowners = PoolOwner.get_items_by_name(PoolOwner, poolowner_name)

            pools = Pool.get_pools_by_poolowners(poolowners)
            pools = Pool.filter_pools(pools, groupowner_id, poolgroup_id, poolowner_id)

        elif filter == 3:
            
            if poolgroup_id == 0:
                poolgroup_id = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).poolgroup_id

            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)

            if poolowners.count() == 0:
                pools = []               
                return poolgroup_id, poolowner_id, pools

            if poolowner_id == 0:
                poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)
            poolowner_name = PoolOwner.get_item_by_id(PoolOwner, poolowner_id).name
            poolowners = PoolOwner.get_items_by_name(PoolOwner, poolowner_name)

            pools = Pool.get_pools_by_poolowners(poolowners)
            pools = Pool.filter_pools(pools, groupowner_id, poolgroup_id, poolowner_id)

        return poolgroup_id, poolowner_id, pools
        
class GroupOwner_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner_id, poolgroup_id, groupowner_id) 

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        groupowner_id = GroupOwner.get_item_by_userid(GroupOwner, site_user.user_id).id
        groupowners = GroupOwner.get_items_by_id(GroupOwner, groupowner_id)
        GroupOwner_Choices.get_choices_by_groupowners(groupowners)

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        poolgroups = PoolGroup.get_poolgroups_with_poolowners(poolgroups)
        if len(poolgroups) == 0:
            viewmodel = {'modelstate':'Error: Create a Pool Group First!'}
            return viewmodel
        PoolGroup_Choices.get_choices_by_poolgroups(poolgroups)

        poolgroup_id = PoolGroup.get_poolgroup_id_if_needed_and_possible(poolgroups, poolgroup_id)

        poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        if poolowners.count() == 0:
            viewmodel = {'modelstate':'Error: Create a Pool Owner First!'}
            return viewmodel
        
        poolowner_id = PoolOwner.get_poolowner_id_if_needed_and_possible(poolowners, poolowner_id)
        PoolOwner_Choices.get_choices_by_poolowners(poolowners)

        cronjobs = CronJob.get_all_items(CronJob)
        CronJob_Choices.get_cronjob_choices(cronjobs)
        cronjob_id = CronJob_Choices.get_all_items(CronJob_Choices)[0].cronjob_id

        pooltypes = PoolType.get_all_items(PoolType)
        PoolType_Choices.get_pooltype_choices(pooltypes)
        pooltype_id = PoolType_Choices.get_all_items(PoolType_Choices)[0].pooltype_id

        if form == None:        
            form = PoolForm_Create(initial = {'cronjob_id': cronjob_id,
                                            'pooltype_id': pooltype_id,
                                            'groupowner_id': groupowner_id,
                                            'poolgroup_id': poolgroup_id,
                                            'poolowner_id' : poolowner_id,
                                            'filter' : filter})

        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        viewmodel = GroupOwner_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class GroupOwner_Edit(Edit_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        pool_id, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            pool_id, poolowner_id, poolgroup_id, groupowner_id)

    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, filter, pool_id, 
        poolowner_id, poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        groupowner_id = pool.poolgroup.groupowner_id
        groupowners = GroupOwner.get_items_by_id(GroupOwner, groupowner_id)
        GroupOwner_Choices.get_choices_by_groupowners(groupowners)

        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        poolgroups = PoolGroup.get_poolgroups_with_poolowners(poolgroups)
        PoolGroup_Choices.get_choices_by_poolgroups(poolgroups)

        poolgroup_id = pool.poolgroup_id

        poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        poolowner_id = pool.poolowner_id
        PoolOwner_Choices.get_choices_by_poolowners(poolowners)

        cronjobs = CronJob.get_all_items(CronJob)
        CronJob_Choices.get_cronjob_choices(cronjobs)
        cronjob_id = pool.cronjob_id

        pooltypes = PoolType.get_all_items(PoolType)
        PoolType_Choices.get_pooltype_choices(pooltypes)
        pooltype_id = pool.pooltype_id

        if form == None:        
            form = PoolForm_Edit(instance = pool, initial = {'filter':filter,
                                                            'groupowner_id':groupowner_id,
                                                            'poolgroup_id':poolgroup_id,
                                                            'poolowner_id':poolowner_id})
        
        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        viewmodel = GroupOwner_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            pool_id, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class GroupOwner_Transfer(Transfer_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        pool, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            pool, poolowner_id, poolgroup_id, groupowner_id)
        
    @classmethod
    def get_transfer_viewmodel(cls, site_user, title, modelstate, filter, pool_id,
        poolowner_id, poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = Pool.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, pool.poolgroup_id)
        PoolOwner_Choices.get_different_choices_than_poolowner(pool.poolowner_id, poolowners)
        poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
        if poolowner_choices.count() == 0:
            viewmodel = {'modelstate':'Error: No other poolowner is in pool group, add a pool owner to pool group first!'}
            return viewmodel

        if form == None:
            form = PoolForm_Transfer(initial={'name' : pool.name,
                                                'new_poolowner_id': poolowner_choices[0].poolowner_id,
                                                'poolgroup_name': pool.poolgroup.name,
                                                'filter' : filter})

        viewmodel = SuperUser_Transfer(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            pool, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class GroupOwner_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, pool_id, 
        poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        viewmodel = GroupOwner_Details(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel


class PoolOwner_Index(Table_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, pools, poolowners, poolgroups, groupowners, 
        filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, pools, poolowners, poolgroups, groupowners, 
            filter, poolowner_id, poolgroup_id, groupowner_id) 

        self.viewmodel['use_pagination'] = False            
        self.viewmodel['user_has_transfer_privileges'] = False

    @classmethod
    def get_index_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolowners = PoolOwner.get_items_by_userid(PoolOwner, site_user.user_id)

        pools = Pool.get_pools_by_poolowners(poolowners)

        poolgroups = PoolGroup.get_poolgroups_by_poolowners(poolowners)

        groupowners = GroupOwner.get_groupowners_by_poolgroups(poolgroups)

        viewmodel = PoolOwner_Index(site_user, title, modelstate, modelsuccess_bool, pools, poolowners, 
            poolgroups, groupowners, filter, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel
        
class PoolOwner_Create(Create_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner_id, poolgroup_id, groupowner_id) 

    @classmethod
    def get_create_viewmodel(cls, site_user, title, modelstate, filter, poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        poolowner = PoolOwner.get_item_by_userid(PoolOwner,site_user.user_id)

        groupowner_id = poolowner.poolgroup.groupowner_id
        groupowners = [poolowner.poolgroup.groupowner]
        GroupOwner_Choices.get_choices_by_groupowners(groupowners)

        poolgroup_id = poolowner.poolgroup_id
        poolgroups = [poolowner.poolgroup]
        PoolGroup_Choices.get_choices_by_poolgroups(poolgroups)

        poolowners = [poolowner]
        PoolOwner_Choices.get_choices_by_poolowners(poolowners)

        cronjobs = CronJob.get_all_items(CronJob)
        CronJob_Choices.get_cronjob_choices(cronjobs)
        cronjob_id = CronJob_Choices.get_all_items(CronJob_Choices)[0].cronjob_id

        pooltypes = PoolType.get_all_items(PoolType)
        PoolType_Choices.get_pooltype_choices(pooltypes)
        pooltype_id = PoolType_Choices.get_all_items(PoolType_Choices)[0].pooltype_id
        
        form = PoolForm_Create(initial = {'cronjob_id': cronjob_id,
                                            'pooltype_id': pooltype_id,
                                            'groupowner_id': groupowner_id,
                                            'poolgroup_id': poolgroup_id,
                                            'poolowner_id' : poolowner.id,
                                            'filter' : filter})

        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        form.fields['poolowner_id'].widget.attrs['disabled'] = 'disabled'

        viewmodel = PoolOwner_Create(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            poolowner.id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class PoolOwner_Edit(Edit_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, form, filter,
        pool_id, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, form, filter,
            pool_id, poolowner_id, poolgroup_id, groupowner_id)

    @classmethod
    def get_edit_viewmodel(cls, site_user, title, modelstate, filter, pool_id, 
        poolowner_id, poolgroup_id, groupowner_id, form):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        poolowner_id = pool.poolowner_id
        poolowners = [pool.poolowner]
        
        poolgroup_id = pool.poolgroup_id
        poolgroups = [pool.poolgroup]

        groupowner_id = pool.poolgroup.groupowner_id
        groupowners = [pool.poolgroup.groupowner]

        GroupOwner_Choices.get_choices_by_groupowners(groupowners)
        PoolGroup_Choices.get_choices_by_poolgroups(poolgroups)
        PoolOwner_Choices.get_choices_by_poolowners(poolowners)

        cronjobs = CronJob.get_all_items(CronJob)        
        CronJob_Choices.get_cronjob_choices(cronjobs)
        cronjob_id = pool.cronjob_id

        pooltypes = PoolType.get_all_items(PoolType)
        PoolType_Choices.get_pooltype_choices(pooltypes)
        pooltype_id = pool.pooltype_id

        if form == None:        
            form = PoolForm_Edit(initial = {'id': pool.id,
                                                'name': pool.name,
                                                'cronjob_id': cronjob_id,
                                                'pooltype_id': pooltype_id,
                                                'groupowner_id': groupowner_id,
                                                'poolgroup_id': poolgroup_id,
                                                'poolowner_id' : poolowner_id,
                                                'filter' : filter})

        form.fields['groupowner_id'].widget.attrs['disabled'] = 'disabled'

        form.fields['poolowner_id'].widget.attrs['disabled'] = 'disabled'

        viewmodel = PoolOwner_Edit(site_user, title, modelstate, modelsuccess_bool, form, filter, 
            pool_id, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel

class PoolOwner_Details(Details_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id) 

    @classmethod
    def get_details_viewmodel(cls, site_user, title, modelstate, filter, pool_id, 
        poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        viewmodel = PoolOwner_Details(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel


class User_Delete(Delete_View):

    def __init__(self, site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id):

        super().__init__(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id) 

    @classmethod
    def get_delete_viewmodel(cls, site_user, title, modelstate, filter,
        pool_id, poolowner_id, poolgroup_id, groupowner_id):

        modelstate, modelsuccess_bool = PoolGroup.get_modelstate(modelstate)

        pool = Pool.get_item_by_id(Pool, pool_id)

        viewmodel = User_Delete(site_user, title, modelstate, modelsuccess_bool, 
            pool, filter, poolowner_id, poolgroup_id, groupowner_id).viewmodel
        
        return viewmodel
