from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from app.mixins import HelperMixins


class CronJobType (models.Model, HelperMixins):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class CronJob (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    cronjobtype = models.ForeignKey(CronJobType, on_delete=models.CASCADE)
    status = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class SiteUser(models.Model, HelperMixins):
    
    name = models.CharField(max_length = 100)
    user_permissions = models.CharField(max_length = 12)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_superuser = models.BooleanField(default = False)
    is_groupowner = models.BooleanField(default = False)
    is_poolowner = models.BooleanField(default = False)
    
    
    def __str__(self):
        return self.name

    @classmethod
    def make_siteuser_superuser(self, site_user):
        site_user.is_superuser = True
        site_user.save()
        return site_user

    @classmethod
    def make_siteuser_groupowner(self, site_user):
        site_user.is_groupowner = True
        site_user.save()
        return site_user
   
    @classmethod
    def delete_siteuser_groupower(self, groupowner):
        site_user = SiteUser.objects.get(user_id = groupowner.user_id)
        site_user.is_groupowner = False
        site_user.save()

    @classmethod
    def delete_siteuser_superuser(self, superuser):
        site_user = SiteUser.objects.get(user_id = superuser.user_id)
        site_user.is_superuser = False
        site_user.save()

class GroupOwner(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def delete_item(cls, groupowner):
        try:
            SiteUser.delete_siteuser_groupower(groupowner)
            groupowner.delete()
            modelstate = 'Success: groupowner, ' + groupowner.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! groupowner, ' + groupowner.name + ' was not deleted!'
        return modelstate

    @classmethod
    def get_groupowner_id_if_needed_and_possible(groupowners, groupowner_id, 
        poolgroup_id, poolowner_id):

        if groupowner_id != None:
            pass
        elif poolowner_id != None:
            groupowner_id = PoolOwner.get_item_by_id( PoolOwner, poolowner_id)
        elif poolgroup_id != None:
            groupowner_id = PoolGroup.get_item_by_id( PoolGroup, poolgroup_id)
        else:
            groupowner_id = groupowners[0].id
        return groupowner_id

    @classmethod
    def get_index_view_model(cls, site_user, modelstate, groupowners):

        modelstate, modelstate_success = GroupOwner.get_modelstate(modelstate)

        view_model = {'title': 'Group Owner Index', # app/layout.html params
                        'site_user':site_user, 
                        'year': datetime.now().year,

                        'partial_view_id': 'groupowner-id', # app/shared_index.html params
                        'modelstate': modelstate, 
                        'modelstate_success': modelstate_success, 
                        'create_item_url': 'groupowner:groupowner_create', 
                        'create_item_name': 'Create Group Owner', 
                        'index_table': 'groupowner/index_table.html', 
                        'scripts': ['app/scripts/Client/TableStripping.js'], 

                        'items': groupowners, # groupowner/index_table.html params
                        'item_label': 'Group Owner Name', 
                        'details_url': 'groupowner:groupowner_details', 
                        'delete_url': 'groupowner:groupowner_delete', 
                        } 
        
        return view_model

    @classmethod
    def get_create_view_model(cls, site_user,form, modelstate):

        modelstate, modelstate_success = GroupOwner.get_modelstate(modelstate)

        view_model = {'title' : 'Create Group Owner', # app/layout.html params
                        'site_user':site_user,
                        'year': datetime.now().year,

                        'partial_view_id': 'superuser-id', # app/shared_create.html params
                        'modelstate': modelstate,
                        'modelstate_success': modelstate_success,
                        'create_form_html': 'groupowner/groupowner_form.html',
                        'create_item_url': 'groupowner:groupowner_create',
                        'index_url': 'groupowner:groupowner_index',
                        'scripts': ['app/scripts/jqueryvalidate.js'],

                        'form': form, # groupowner/groupowner_form.html params
                        'form_label_name': 'Group Owner Name'} 

        return view_model

    @classmethod
    def get_details_and_delete_view_model(cls, site_user, title, groupowner):
        view_model = {'title': title, # app/layout.html params
                        'site_user':site_user,
                        'year': datetime.now().year,

                        'descriptive_list': 'groupowner/descriptive_list.html', # app/shared_details.html and app/shared_delete params.html
                        'delete_url': 'groupowner:groupowner_delete',
                        'index_url': 'groupowner:groupowner_index',
 
                        'item': groupowner, # groupowner/descriptive_list.html params
                        'list_label_name': 'Group Owner Name',
                        'list_label_email': 'E-mail'}

        return view_model

class SuperUser(models.Model, HelperMixins):
    
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def delete_item(cls, superuser):
        try:
            SiteUser.delete_siteuser_superuser(superuser)
            superuser.delete()
            modelstate = 'Success: Superuser, ' + superuser.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! Superuser, ' + superuser.name + ' was not deleted!'
        return modelstate

    @classmethod
    def get_index_view_model(cls, site_user, modelstate, superusers):

        modelstate, modelstate_success = SuperUser.get_modelstate(modelstate)

        view_model = {'site_user':site_user, # app/layout.html params
                        'title': 'Super User Index',
                        'year': datetime.now().year,

                        'partial_view_id': 'superuser-id', # app/shared_index.html params
                        'modelstate_success': modelstate_success,
                        'modelstate': modelstate,
                        'scripts': ['app/scripts/Client/TableStripping.js'],
                        'create_item_url': 'superuser:superuser_create',
                        'create_item_name': 'Create Super User',
                        'index_table': 'superuser/index_table.html',

                        'items': superusers, # super_user/index_table.html params
                        'item_label': 'Super User Name', 
                        'details_url': 'superuser:superuser_details', 
                        'delete_url': 'superuser:superuser_delete',}
        
        return view_model

    @classmethod
    def get_create_view_model(cls, site_user,form, modelstate):

        modelstate, modelstate_success = SuperUser.get_modelstate(modelstate)

        view_model = {'title' : 'Create Super User', # layout params
                        'site_user':site_user,
                        'year': datetime.now().year,

                        'partial_view_id': 'superuser-id', # shared_create params
                        'modelstate': modelstate,
                        'modelstate_success': modelstate_success,
                        'create_item_url': 'superuser:superuser_create',
                        'create_form_html': 'superuser/superuser_form.html',
                        'index_url': 'superuser:superuser_index',
                        'scripts': ['app/scripts/jqueryvalidate.js'],

                        'form': form, # superuser_form params
                        'form_label_name': 'Super User Name'} 


        return view_model

    @classmethod
    def get_details_and_delete_view_model(cls, site_user, title, superuser):
        view_model = {'title': title, # app/layout.html params
                        'site_user':site_user,
                        'year': datetime.now().year,
 
                        'descriptive_list': 'superuser/descriptive_list.html', # app/shared_create.html params
                        'delete_url': 'superuser:superuser_delete',
                        'index_url': 'superuser:superuser_index',

                        'item': superuser, # super_user/descriptive_list.html params
                        'list_label_name': 'Super User Name',
                        'list_label_email': 'E-mail'}
        return view_model

class PoolGroup (models.Model, HelperMixins):
    name = models.CharField(max_length = 50)
    groupowner = models.ForeignKey(GroupOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PoolOwner (models.Model, HelperMixins):
    name = models.CharField(max_length = 50)
    poolgroup = models.ForeignKey(PoolGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.name

class PoolType (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Pool (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)

    poolgroup = models.ForeignKey(PoolGroup, on_delete = models.CASCADE)
    poolowner = models.ForeignKey(PoolOwner, on_delete = models.DO_NOTHING)
    pooltype = models.ForeignKey(PoolType, on_delete = models.DO_NOTHING)
    cronjob = models.ForeignKey(CronJob, on_delete = models.DO_NOTHING, null = True)

    def __str__(self):
        return self.name
