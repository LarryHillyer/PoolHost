from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolGroup, GroupOwner, SuperUser
from app.mixins import HelperMixins

class Index_ViewModel(PoolGroup):

    def __init__(self, site_user, modelstate, modelstate_bool, poolgroups, filter,
        groupowner_id):

        self.viewmodel ={'title': 'Pool Group Index', # app/layout.html params
                        'site_user':site_user, 
                        'year': datetime.now().year,

                        'partial_view_id': 'poolgroup-id', # app/shared_index_pagination.html params
                        'groupowner_id': groupowner_id,
                        'filter' : filter,
                        'modelstate': modelstate, 
                        'modelstate_bool': modelstate_bool, 
                        'create_url': 'poolgroup:create', 
                        'create_name': 'Create Pool Group', 
                        'index_table': 'poolgroup/index_table.html', 
                        'scripts': ['app/scripts/Client/TableStripping.js'],
 
                        'items': poolgroups, # poolgroup/index_table.html params
                        'header_label_item': 'Pool Group Name',
                        'item_url': 'poolowner:index',
                        'edit_url': 'poolgroup:edit',
                        'details_url': 'poolgroup:details', 
                        'delete_url': 'poolgroup:delete', 
                        }

    @classmethod
    def get_groupowner_id_poolgroups(cls, filter, groupowners, groupowner_id):

        if filter == None or filter == 0:
            groupowner_id = None
            poolgroups = PoolGroup.get_all_items(PoolGroup)
        else:    
            groupowner_id = GroupOwner.get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id)       

            if groupowner_id != None:
                poolgroups = Index_ViewModel.filter_poolgroups(groupowner_id)

        return groupowner_id, poolgroups

    @classmethod
    def filter_poolgroups(poolgroup_id = None, groupowner_id = None):

        if poolgroup_id != None:
            poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)
        elif groupowner_id != None:
            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        
        return poolgroups

class SuperUser_Index(Index_ViewModel):

    def __init__(self, site_user, modelstate, modelstate_bool, poolgroups, filter,
        groupowner_id, groupowners):

        super().__init__(site_user, modelstate, modelstate_bool, poolgroups, filter,
            groupowner_id) 

        self.viewmodel['use_pagination'] = True  # app/shared_index_pagination.html          
        self.viewmodel['pagination'] = 'app/user_navigation.html'  

        self.viewmodel['superuser_pagination'] = 'poolgroup/superuser_pagination.html' #app/user_navigation.html
        self.viewmodel['groupowner_pagination'] = 'poolgroup/groupowner_pagination.html'
        self.viewmodel['shared_groupowner_pagination'] = 'app/groupowner_pagination.html'
        self.viewmodel['shared_poolgroup_pagination'] = 'app/poolgroup_pagination.html'
        self.viewmodel['shared_poolowner_pagination'] = 'app/poolowner_pagination.html'

                        
        self.viewmodel['model_groupowners'] = groupowners #poolgroup/superuser_pagination.html
        self.viewmodel['index_url'] = 'poolgroup:index'

        self.viewmodel['header_label_groupowner'] = 'Group Owner Name' # poolgroup/index_table.html 

    @classmethod
    def get_index_viewmodel(cls, site_user, modelstate, groupowner_id = None, filter = None):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)

        groupowners = GroupOwner.get_all_items(GroupOwner)
        groupowner_id, poolgroups = Index_ViewModel.get_groupowner_id_poolgroups(filter, groupowners, groupowner_id)

        viewmodel = SuperUser_Index(site_user, modelstate, modelstate_bool, poolgroups, filter, groupowner_id, groupowners).viewmodel
        
        return viewmodel

class GroupOwner_Index(Index_ViewModel):

    def __init__(self, site_user, modelstate, modelstate_bool, poolgroups, filter,
        groupowner_id):

        super().__init__(site_user, modelstate, modelstate_bool, poolgroups, filter,
            groupowner_id) 

        self.viewmodel['use_pagination'] = False  # app/shared_index_pagination.html          

    @classmethod
    def get_index_viewmodel(cls, site_user, modelstate, groupowner_id, filter = None):

        modelstate, modelstate_bool = PoolGroup.get_modelstate(modelstate)
        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

        viewmodel = GroupOwner_Index(site_user, modelstate, modelstate_bool, poolgroups, filter, groupowner_id).viewmodel
        
        return viewmodel
