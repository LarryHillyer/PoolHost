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

    @classmethod
    def get_exactly_same_cronjobtype(cls, cronjobtype_id, cronjobtype_name):
        exactly_same_cronjobtype = None
        try:
            exactly_same_cronjobtype = PoolType.objects.filter(id = cronjobtype_id, name=cronjobtype_name)
        except:
            pass
        return exactly_same_cronjobtype

    @classmethod
    def get_same_cronjobtype_in_database(cls, cronjobtype_name):
        same_cronjobtype = None
        try:
            same_cronjobtype = PoolType.objects.filter(name=cronjobtype_name)
        except:
            pass
        return same_cronjobtype

class CronJobType_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    cronjobtype_id = models.IntegerField()

    @classmethod
    def get_cronjobtype_choices(cls, cronjobtype_id = 0):

        try:

            if cronjobtype_id == 0:
                cronjobtypes = CronJobType.get_all_items(CronJobType)
            else:
                cronjobtypes = CronJobType.get_items_by_id(CronJobType, cronjobtype_id)

            cronjobtype_choices = CronJobType_Choices.get_all_items(CronJobType_Choices)
            if cronjobtype_choices.count() > 0:               
                cronjobtype_choices.delete()
            for cronjobtype in cronjobtypes:
                cronjobtype_choice = CronJobType_Choices(name = cronjobtype.name, cronjobtype_id = cronjobtype.id)
                CronJobType_Choices.add_item(CronJobType_Choices, cronjobtype_choice)
        except:
            pass


    @classmethod
    def make_cronjobtype_choices(cls):
        cronjobtype_choices_1 = CronJobType_Choices.get_all_items(CronJobType_Choices)
        cronjobtype_choices = []
        for cronjobtype_choice in cronjobtype_choices_1:
            cronjobtype_choices.append((cronjobtype_choice.cronjobtype_id, cronjobtype_choice.name))
        return cronjobtype_choices

class CronJob (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    cronjobtype = models.ForeignKey(CronJobType, on_delete=models.CASCADE)
    status = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_cronjob(cls, cronjob_id, cronjob_name, cronjob_cronjobtype_id):
        exactly_same_cronjob = None
        try:
            exactly_same_cronjob = CronJob.objects.filter(id = cronjob_id, name=cronjob_name, 
                cronjobtype_id = cronjob_cronjobtype_id)
        except:
            pass
        return exactly_same_cronjob

    @classmethod
    def get_same_cronjob_in_database(cls, cronjob_name):
        same_cronjob = None
        try:
            same_cronjob = CronJob.objects.filter(name=cronjob_name)
        except:
            pass
        return same_cronjob


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
    def get_groupowner_choices_2(cls, groupowner_id = 0):

        try:

            groupowners = GroupOwner.get_all_items(GroupOwner)

            groupowner_choices = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
            if groupowner_choices.count() > 0:               
                groupowner_choices.delete()
            for groupowner in groupowners:
                if groupowner.id != groupowner_id:
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
    def get_poolgroup_choices_by_groupowner_id(cls, groupowner_id, poolgroup_id = 0):

        try:

            poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)

            poolgroup_choices = PoolGroup_Choices.get_all_items(PoolGroup_Choices)
            if poolgroup_choices.count() > 0:               
                poolgroup_choices.delete()
            for poolgroup in poolgroups:
                if poolgroup.id != poolgroup_id:
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

    @classmethod
    def get_poolowner_id_if_needed_and_possible(cls, poolowners, poolowner_id, 
        pool_id = 0):

        if poolowner_id != 0:
            pass
        elif pool_id != 0:
            pool = Pool.get_item_by_id( Pool, pool_id)
            poolowner_id = pool.poolowner_id 
        else:
            poolowner_id = poolowners[0].id

        return poolowner_id


class PoolOwner_Choices(models.Model, HelperMixins):
    
    name = models.CharField(max_length = 50)
    poolowner_id = models.IntegerField()

    @classmethod
    def get_poolowner_choices(cls, poolowner_id = 0):

        try:

            if poolowner_id == 0:
                poolowners = PoolOwner.get_all_items(PoolOwner)
            else:
                poolowners = PoolOwner.get_items_by_id(PoolOwner, poolowner_id)

            poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
            if poolowner_choices.count() > 0:               
                poolowner_choices.delete()
            for poolowner in poolowners:
                poolowner_choice = PoolOwner_Choices(name = poolowner.name, poolowner_id = poolowner.id)
                PoolOwner_Choices.add_item(PoolOwner_Choices, poolowner_choice)
        except:
            pass

    @classmethod
    def get_poolowner_choices_by_poolgroup_id(cls, poolgroup_id, poolowner_id = 0):

        try:

            poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)

            poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
            if poolowner_choices.count() > 0:               
                poolowner_choices.delete()
            for poolowner in poolowners:
                if poolowner.id != poolowner_id:
                    poolowner_choice = PoolOwner_Choices(name = poolowner.name, poolowner_id = poolowner.id)
                    PoolOwner_Choices.add_item(PoolOwner_Choices, poolowner_choice)
        except:
            pass

    @classmethod
    def make_poolowner_choices(cls):
        poolowner_choices_1 = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
        poolowner_choices = []
        for poolowner_choice in poolowner_choices_1:
            poolowner_choices.append((poolowner_choice.poolowner_id, poolowner_choice.name))
        return poolowner_choices

class PoolType (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_pooltype(cls, pooltype_id, pooltype_name):
        exactly_same_pooltype = None
        try:
            exactly_same_pooltype = PoolType.objects.filter(id = pooltype_id, name=pooltype_name)
        except:
            pass
        return exactly_same_pooltype

    @classmethod
    def get_same_pooltype_in_database(cls, pooltype_name):
        same_pooltype = None
        try:
            same_pooltype = PoolType.objects.filter(name=pooltype_name)
        except:
            pass
        return same_pooltype

class Pool (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)

    poolgroup = models.ForeignKey(PoolGroup, on_delete = models.CASCADE)
    poolowner = models.ForeignKey(PoolOwner, on_delete = models.DO_NOTHING)
    pooltype = models.ForeignKey(PoolType, on_delete = models.DO_NOTHING)
    cronjob = models.ForeignKey(CronJob, on_delete = models.DO_NOTHING, null = True)

    def __str__(self):
        return self.name
