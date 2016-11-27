from datetime import datetime
import json

from django.db import models
from django.contrib.auth.models import User
from django.core.serializers import serialize

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
    def delete_siteuser_groupowner(self, groupowner):
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
            SiteUser.delete_siteuser_groupowner(groupowner)
            groupowner.delete()
            modelstate = 'Success: groupowner, ' + groupowner.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! groupowner, ' + groupowner.name + ' was not deleted!'
        return modelstate
    
    @classmethod
    def get_groupowner_id_if_needed_and_possible(cls, groupowners, groupowner_id, 
        poolgroup_id = 0, poolowner_id = 0):

        if groupowner_id != 0:
            pass
        elif poolowner_id != 0:
            poolowner = PoolOwner.get_item_by_id( PoolOwner, poolowner_id)
            groupowner_id = poolowner.poolgroup.groupowner_id
        elif poolgroup_id != 0:
            poolgroup = PoolGroup.get_item_by_id( PoolGroup, poolgroup_id)
            groupowner_id = poolgroup.groupowner_id
        else:
            groupowner_id = groupowners[0].id
        return groupowner_id

class GroupOwner_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    groupowner_id = models.IntegerField()

    @classmethod
    def get_groupowner_choices(cls, groupowner_id = 0):

        try:

            if groupowner_id == 0:
                groupowners = GroupOwner.get_all_items(GroupOwner)
            else:
                groupowners = GroupOwner.get_items_by_id(GroupOwner, groupowner_id)

            groupowner_choices = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
            if groupowner_choices.count() > 0:               
                groupowner_choices.delete()
            for groupowner in groupowners:
                groupowner_choice = GroupOwner_Choices(name = groupowner.name, groupowner_id = groupowner.id)
                GroupOwner_Choices.add_item(GroupOwner_Choices, groupowner_choice)
        except:
            pass

    @classmethod
    def make_groupowner_choices(cls):
        groupowner_choices_1 = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
        groupowner_choices = []
        for groupowner_choice in groupowner_choices_1:
            groupowner_choices.append((groupowner_choice.groupowner_id, groupowner_choice.name))
        return groupowner_choices

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

class PoolGroup (models.Model, HelperMixins):
    name = models.CharField(max_length = 50)
    groupowner = models.ForeignKey(GroupOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_poolgroup(cls, poolgroup_id, poolgroup_name, poolgroup_groupowner_id):
        exactly_same_poolgroup = None
        try:
            exactly_same_poolgroup = PoolGroup.objects.filter(id = poolgroup_id, name=poolgroup_name, 
                groupowner_id = poolgroup_groupowner_id)
        except:
            pass
        return exactly_same_poolgroup

    @classmethod
    def get_same_poolgroup_in_database(cls, poolgroup_name, poolgroup_groupowner_id):
        same_poolgroup = None
        try:
            same_poolgroup = PoolGroup.objects.filter(name=poolgroup_name, groupowner_id = poolgroup_groupowner_id)
        except:
            pass
        return same_poolgroup

    @classmethod
    def transfer_group_ownership(cls, poolgroups, new_groupowner_id, modelstate):
        error = None
        for poolgroup in poolgroups:
            poolgroup.groupowner_id = new_groupowner_id
            modelstate = PoolGroup.edit_item(PoolGroup, poolgroup)
            if modelstate.split(':')[0] != 'Success':
                error = 'Error'
        if error == None:
            return 'Success: Group ownership was transfered'
        else:
            return 'Error: Database Error must be investigated'

    @classmethod
    def get_poolgroup_id_if_needed_and_possible(cls, poolgroups, poolgroup_id, 
        poolowner_id = 0):

        if poolgroup_id != 0:
            pass
        elif poolowner_id != 0:
            poolowner = PoolOwner.get_item_by_id( PoolOwner, poolowner_id)
            poolgroup_id = poolowner.poolgroup_id 
        else:
            poolgroup_id = poolgroups[0].id

        return poolgroup_id

    @classmethod
    def get_poolgroups_by_groupowner_id(cls, groupowner_id):
        
        poolgroups = []
        poolgroups_set = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        for poolgroup in poolgroups_set:
            poolgroups.append({'id' : poolgroup.id, 'name': poolgroup.name})
        return json.dumps(poolgroups)


class PoolGroup_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    poolgroup_id = models.IntegerField()

    @classmethod
    def get_poolgroup_choices(cls, poolgroup_id = 0):

        try:

            if poolgroup_id == 0:
                poolgroups = PoolGroup.get_all_items(PoolGroup)
            else:
                poolgroups = PoolGroup.get_items_by_id(PoolGroup, poolgroup_id)

            poolgroup_choices = PoolGroup_Choices.get_all_items(PoolGroup_Choices)
            if poolgroup_choices.count() > 0:               
                poolgroup_choices.delete()
            for poolgroup in poolgroups:
                poolgroup_choice = PoolGroup_Choices(name = poolgroup.name, poolgroup_id = poolgroup.id)
                PoolGroup_Choices.add_item(PoolGroup_Choices, poolgroup_choice)
        except:
            pass

    @classmethod
    def get_poolgroup_choices_by_groupowner_id(cls, groupowner_id):

        try:

            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

            poolgroup_choices = PoolGroup_Choices.get_all_items(PoolGroup_Choices)
            if poolgroup_choices.count() > 0:               
                poolgroup_choices.delete()
            for poolgroup in poolgroups:
                poolgroup_choice = PoolGroup_Choices(name = poolgroup.name, poolgroup_id = poolgroup.id)
                PoolGroup_Choices.add_item(PoolGroup_Choices, poolgroup_choice)
        except:
            pass

    @classmethod
    def make_poolgroup_choices(cls):
        poolgroup_choices_1 = PoolGroup_Choices.get_all_items(PoolGroup_Choices)
        poolgroup_choices = []
        for poolgroup_choice in poolgroup_choices_1:
            poolgroup_choices.append((poolgroup_choice.poolgroup_id, poolgroup_choice.name))
        return poolgroup_choices



class PoolOwner (models.Model, HelperMixins):
    name = models.CharField(max_length = 50)
    poolgroup = models.ForeignKey(PoolGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.name

    @classmethod
    def get_items_by_groupowner_id(cls, model_cls, model_groupowner_id):
        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, model_groupowner_id)
        poolowners = []
        for poolgroup in poolgroups:
            poolgroup_poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup.id)
            for poolowner in poolgroup_poolowners:
                poolowners.append(poolowner)
        return poolowners

    @classmethod
    def is_poolowner_siteuser(cls, poolowner_name):

        site_user = SiteUser.get_item_by_name(SiteUser, poolowner_name)
        if site_user == None:
            return False
        else:
            return True

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
