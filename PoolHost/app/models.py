from datetime import datetime
import json

from django.db import models
from django.contrib.auth.models import User
from django.core.serializers import serialize

from app.mixins import HelperMixins


class SiteUser(models.Model, HelperMixins):
    
    name = models.CharField(max_length = 100)
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
    def make_siteuser_poolowner(self, site_user):
        site_user.is_poolowner = True
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

    @classmethod
    def delete_siteuser_poolowner(self, poolowner):
        site_user = SiteUser.objects.get(user_id = poolowner.user_id)
        site_user.is_poolowner = False
        site_user.save()


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


class CronJobType (models.Model, HelperMixins):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_cronjobtype(cls, cronjobtype_id, cronjobtype_name):
        exactly_same_cronjobtype = None
        try:
            exactly_same_cronjobtype = CronJobType.objects.filter(id = cronjobtype_id, name=cronjobtype_name)
        except:
            pass
        return exactly_same_cronjobtype

    @classmethod
    def get_same_cronjobtype_in_database(cls, cronjobtype_name):
        same_cronjobtype = None
        try:
            same_cronjobtype = CronJobType.objects.filter(name=cronjobtype_name)
        except:
            pass
        return same_cronjobtype

class CronJobType_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    cronjobtype_id = models.IntegerField()

    @classmethod
    def get_cronjobtype_choices(cls, cronjobtypes):

        cronjobtype_choices = CronJobType_Choices.get_all_items(CronJobType_Choices)
        if cronjobtype_choices.count() > 0:               
            cronjobtype_choices.delete()
        for cronjobtype in cronjobtypes:
            cronjobtype_choice = CronJobType_Choices(name = cronjobtype.name, cronjobtype_id = cronjobtype.id)
            CronJobType_Choices.add_item(CronJobType_Choices, cronjobtype_choice)


    @classmethod
    def make_cronjobtype_choices(cls):
        cronjobtype_choices_1 = CronJobType_Choices.get_all_items(CronJobType_Choices)
        cronjobtype_choices = []
        for cronjobtype_choice in cronjobtype_choices_1:
            cronjobtype_choices.append((cronjobtype_choice.cronjobtype_id, cronjobtype_choice.name))
        return cronjobtype_choices


class GroupOwner(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    @classmethod
    def delete_item(cls, groupowner):
        try:
            SiteUser.delete_siteuser_groupowner(groupowner)
            PoolGroup.delete_groupowner_poolgroups(groupowner.id)
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
        elif groupowners != []:
            groupowner_id = groupowners[0].id
        return groupowner_id

    @classmethod
    def get_groupowners_by_poolgroups(cls, poolgroups):
        groupowners = []
        for poolgroup in poolgroups:
            groupowner = GroupOwner.get_item_by_id(GroupOwner, poolgroup.groupowner_id)
            groupowners.append(groupowner)
        return groupowners

    @classmethod
    def get_groupowners_with_poolowners(cls, groupowners):
        groupowners_with_poolowners = []
        for groupowner in groupowners:
            groupowner_poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner.id)
            for groupowner_poolgroup in groupowner_poolgroups:
                poolgroup_poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, groupowner_poolgroup.id)
                if poolgroup_poolowners.count() > 0:
                    groupowners_with_poolowners.append(groupowner)
                    break
        return groupowners_with_poolowners

    @classmethod
    def get_groupowners_with_poolgroups(cls, groupowners):
        groupowners_with_poolgroups = []
        for groupowner in groupowners:
            groupowner_poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner.id)
            if groupowner_poolgroups.count() > 0:
                groupowners_with_poolgroups.append(groupowner)
        return groupowners_with_poolgroups

class GroupOwner_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    groupowner_id = models.IntegerField()

    @classmethod
    def get_choices_by_groupowners(cls, groupowners):
            groupowner_choices = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
            if groupowner_choices.count() > 0:               
                groupowner_choices.delete()
            for groupowner in groupowners:
                groupowner_choice = GroupOwner_Choices(name = groupowner.name, groupowner_id = groupowner.id)
                GroupOwner_Choices.add_item(GroupOwner_Choices, groupowner_choice)

    @classmethod
    def get_different_choices_than_groupowner(cls, groupowner_id, groupowners):
        groupowner_choices = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
        if groupowner_choices.count() > 0:               
            groupowner_choices.delete()
        for groupowner in groupowners:
            if groupowner.id != groupowner_id:
                groupowner_choice = GroupOwner_Choices(name = groupowner.name, groupowner_id = groupowner.id)
                GroupOwner_Choices.add_item(GroupOwner_Choices, groupowner_choice)

    @classmethod
    def make_groupowner_choices(cls):
        groupowner_choices_1 = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
        groupowner_choices = []
        for groupowner_choice in groupowner_choices_1:
            groupowner_choices.append((groupowner_choice.groupowner_id, groupowner_choice.name))
        return groupowner_choices


class PoolGroup (models.Model, HelperMixins):
    name = models.CharField(max_length = 50)
    groupowner = models.ForeignKey(GroupOwner, on_delete=models.CASCADE)

    class Meta:
        ordering = ['groupowner']

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
            return 'Error: Group ownership was not transfered'

    @classmethod
    def get_poolgroup_id_if_needed_and_possible(cls, poolgroups, poolgroup_id, 
        poolowner_id = 0):

        if poolgroup_id != 0:
            pass
        elif poolowner_id != 0:
            poolowner = PoolOwner.get_item_by_id( PoolOwner, poolowner_id)
            poolgroup_id = poolowner.poolgroup_id 
        elif poolgroups != []:
            poolgroup_id = poolgroups[0].id

        return poolgroup_id

    @classmethod
    def get_poolgroups_with_poolowners_by_groupowner_id(cls, groupowner_id):
        
        poolgroups = []
        poolgroups_set = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        poolgroups_set = PoolGroup.get_poolgroups_with_poolowners(poolgroups_set)
        for poolgroup in poolgroups_set:
            poolgroups.append({'id' : poolgroup.id, 'name': poolgroup.name})
        return json.dumps(poolgroups)

    @classmethod
    def get_poolgroups_by_groupowner_id_2(cls, groupowner_id):
        
        poolgroups = []
        poolgroups_set = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        for poolgroup in poolgroups_set:
            poolgroups.append({'id' : poolgroup.id, 'name': poolgroup.name})
        return json.dumps(poolgroups)

    @classmethod
    def get_poolgroups_by_poolowners(cls, poolowners):

        poolgroups = []
        for poolowner in poolowners:
            poolgroup = PoolGroup.get_item_by_id(PoolGroup,poolowner.poolgroup_id)
            poolgroups.append(poolgroup)
        return poolgroups

    @classmethod
    def delete_poolgroup_poolowners(cls, poolgroup_id):

        poolgroup_poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        for poolgroup_poolowner in poolgroup_poolowners:
            try:
                Pool.delete_poolowner_pools(poolgroup_poolowner.id)
                PoolOwner.delete_item(poolgroup_poolowner)
                modelstate = 'Success: ' + poolgroup_poolowner.name + ' has been deleted!'
            except:
                modelstate = 'Error: Database Error!!! ' + poolgroup_poolowner.name + ' was not deleted!'

            return modelstate

    @classmethod
    def delete_groupowner_poolgroups(cls, groupowner_id):
        modelstate = None
        groupowner_poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner_id)
        for groupowner_poolgroup in groupowner_poolgroups:
            modelstate = PoolGroup.delete_item(groupowner_poolgroup)

        return modelstate

    @classmethod
    def delete_item(cls, poolgroup):
        try:
            PoolGroup.delete_poolgroup_poolowners(poolgroup.id)
            modelstate = PoolGroup.delete(poolgroup)
            modelstate = 'Success: ' + poolgroup.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! ' + poolgroup.name + ' was not deleted!'
        return modelstate

    @classmethod
    def get_poolgroups_with_poolowners(cls, poolgroups):
        poolgroups_with_poolowners = []
        for poolgroup in poolgroups:
            poolgroup_poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup.id)
            if poolgroup_poolowners.count() > 0:
                poolgroups_with_poolowners.append(poolgroup)
        return poolgroups_with_poolowners

class PoolGroup_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    poolgroup_id = models.IntegerField()

    @classmethod
    def get_choices_by_poolgroups(cls, poolgroups):

        poolgroup_choices = PoolGroup_Choices.get_all_items(PoolGroup_Choices)
        if poolgroup_choices.count() > 0:               
            poolgroup_choices.delete()
        for poolgroup in poolgroups:
            poolgroup_choice = PoolGroup_Choices(name = poolgroup.name, poolgroup_id = poolgroup.id)
            PoolGroup_Choices.add_item(PoolGroup_Choices, poolgroup_choice)

    @classmethod
    def get_different_choices_than_poolgroup(cls, poolgroup_id, poolgroups):

        poolgroup_choices = PoolGroup_Choices.get_all_items(PoolGroup_Choices)
        if poolgroup_choices.count() > 0:               
            poolgroup_choices.delete()
        for poolgroup in poolgroups:
            if poolgroup.id != poolgroup_id:
                poolgroup_choice = PoolGroup_Choices(name = poolgroup.name, poolgroup_id = poolgroup.id)
                PoolGroup_Choices.add_item(PoolGroup_Choices, poolgroup_choice)

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

    class Meta:
        ordering = ['poolgroup']

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
        elif poolowners != []:
            poolowner_id = poolowners[0].id

        return poolowner_id

    @classmethod
    def get_poolowner_by_poolgroup_id_and_name(cls, poolgroup_id, poolowner_name):
        poolowners = []
        poolowners_set = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        for poolowner in poolowners_set:
            if poolowner.name == poolowner_name:
                poolowners.append({'id' : poolowner.id, 'name': poolowner.name})
        return json.dumps(poolowners)

    @classmethod
    def get_poolowners_by_poolgroup_id(cls, poolgroup_id):
        
        poolowners = []
        poolowners_set = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup_id)
        for poolowner in poolowners_set:
            poolowners.append({'id' : poolowner.id, 'name': poolowner.name})
        return json.dumps(poolowners)

    @classmethod
    def get_poolowners_by_groupowners(cls, groupowners):

        poolowners = []
        for groupowner in groupowners:
            groupowner_poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, groupowner.id)
            for groupowner_poolgroup in groupowner_poolgroups:
                groupowner_poolgroup_poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, groupowner_poolgroup.id)
                for groupowner_poolgroup_poolowner in groupowner_poolgroup_poolowners:
                    poolowners.append(groupowner_poolgroup_poolowner)

        return poolowners

    @classmethod
    def get_poolowners_by_poolgroups(cls, poolgroups):

        poolowners = []
        for poolgroup in poolgroups:
            poolgroup_poolowners = PoolOwner.get_items_by_poolgroup_id(PoolOwner, poolgroup.id)
            for poolgroup_poolowner in poolgroup_poolowners:
                poolowners.append(poolgroup_poolowner)

        return poolowners

    @classmethod
    def delete_item(cls, poolowner):
        poolowners = PoolOwner.get_items_by_name(PoolOwner, poolowner.name)
        if poolowners.count() == 1:
            old_poolowner = SiteUser.get_item_by_userid(SiteUser, poolowner.user_id)
            SiteUser.delete_siteuser_poolowner(old_poolowner)
        Pool.delete_poolowner_pools(poolowner.id)
        try:
            PoolOwner.delete(poolowner)
            modelstate = 'Success: ' + poolowner.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! ' + poolowner.name + ' was not deleted!'
        return modelstate

class PoolOwner_Choices(models.Model, HelperMixins):
    
    name = models.CharField(max_length = 50)
    poolowner_id = models.IntegerField()


    @classmethod
    def get_choices_by_poolowners(cls, poolowners):

        poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
        if poolowner_choices.count() > 0:               
            poolowner_choices.delete()
        for poolowner in poolowners:
            poolowner_choice = PoolOwner_Choices(name = poolowner.name, poolowner_id = poolowner.id)
            PoolOwner_Choices.add_item(PoolOwner_Choices, poolowner_choice)

    @classmethod
    def get_different_choices_than_poolowner(cls, poolowner_id, poolowners):

        poolowner_choices = PoolOwner_Choices.get_all_items(PoolOwner_Choices)
        if poolowner_choices.count() > 0:               
            poolowner_choices.delete()
        for poolowner in poolowners:
            if poolowner.id != poolowner_id:
                poolowner_choice = PoolOwner_Choices(name = poolowner.name, poolowner_id = poolowner.id)
                PoolOwner_Choices.add_item(PoolOwner_Choices, poolowner_choice)

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

class PoolType_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    pooltype_id = models.IntegerField()

    @classmethod
    def get_pooltype_choices(cls, pooltypes):

        pooltype_choices = PoolType_Choices.get_all_items(PoolType_Choices)
        if pooltype_choices.count() > 0:               
            pooltype_choices.delete()
        for pooltype in pooltypes:
            pooltype_choice = PoolType_Choices(name = pooltype.name, pooltype_id = pooltype.id)
            PoolType_Choices.add_item(PoolType_Choices, pooltype_choice)


    @classmethod
    def make_pooltype_choices(cls):
        pooltype_choices_1 = PoolType_Choices.get_all_items(PoolType_Choices)
        pooltype_choices = []
        for pooltype_choice in pooltype_choices_1:
            pooltype_choices.append((pooltype_choice.pooltype_id, pooltype_choice.name))
        return pooltype_choices


class Sport(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_sport(cls, sport_id, sport_name):
        exactly_same_sport = None
        try:
            exactly_same_sport = Sport.objects.filter(id = sport_id, name=sport_name)
        except:
            pass
        return exactly_same_sport

    @classmethod
    def get_same_sport_in_database(cls, sport_name):
        same_sport = None
        try:
            same_sport = Sport.objects.filter(name=sport_name)
        except:
            pass
        return same_sport

    @classmethod
    def get_sport_id_if_needed_and_possible(cls, sports, sport_id, 
        league_id = 0, nfl_conference_id = 0):

        if sport_id != 0:
            pass

        elif nfl_conference_id != 0:
            nfl_conference = NFL_Conference.get_item_by_id( NFL_Conference, poolowner_id)
            sport_id = nfl_conference.league.sport_id

        elif league_id != 0:
            league = PoolGroup.get_item_by_id( PoolGroup, league_id)
            sport_id = league.sport_id
        elif sports != []:
            sport_id = sports[0].id
        return sport_id

    @classmethod
    def get_sports_by_leagues(cls, leagues):
        sports = []
        for league in leagues:
            sport = Sport.get_item_by_id(Sport, league.sport_id)
            sports.append(sport)
        return sports

    @classmethod
    def get_sports_with_leagues(cls, sports):
        sports_with_leagues = []
        for sport in sports:
            sport_leagues = League.get_items_by_sport_id(League, sport.id)
            if sport_leagues.count() > 0:
                sports_with_leagues.append(sport)
        return sports_with_leagues

class Sport_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    sport_id = models.IntegerField()

    @classmethod
    def get_choices_by_sports(cls, sports):
            sport_choices = Sport_Choices.get_all_items(Sport_Choices)
            if sport_choices.count() > 0:               
                sport_choices.delete()
            for sport in sports:
                sport_choice = Sport_Choices(name = sport.name, sport_id = sport.id)
                Sport_Choices.add_item(Sport_Choices, sport_choice)

    @classmethod
    def make_sport_choices(cls):
        sport_choices_1 = Sport_Choices.get_all_items(Sport_Choices)
        sport_choices = []
        for sport_choice in sport_choices_1:
            sport_choices.append((sport_choice.sport_id, sport_choice.name))
        return sport_choices


class League(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    league_icon_path = models.CharField(max_length = 250)
    league_label_path = models.CharField(max_length = 250)
    sport = models.ForeignKey(Sport, on_delete = models.CASCADE)

    class Meta:
        ordering = ['sport']

    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_league(cls, league_id, league_name, league_sport_id):
        exactly_same_league = None
        try:
            exactly_same_league = League.objects.filter(id = league_id, name=league_name, 
                sport_id = league_sport_id)
        except:
            pass
        return exactly_same_league

    @classmethod
    def get_same_league_in_database(cls, league_name, league_sport_id):
        same_league = None
        try:
            same_league = League.objects.filter(name=league_name, sport_id = league_sport_id)
        except:
            pass
        return same_league

    @classmethod
    def delete_item(cls, league):
        try:
            #League.delete_league_conferences(league.id)
            modelstate = League.delete(league)
            modelstate = 'Success: ' + league.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! ' + league.name + ' was not deleted!'
        return modelstate

    @classmethod
    def get_league_id_if_needed_and_possible(cls, leagues, league_id, 
        conference_id = 0):

        if league_id != 0:
            pass
        elif conference_id != 0:
            conference = NFL_Conference.get_item_by_id(NFL_Conference, conference_id)
            league_id = conference.league_id 
        elif leagues != []:
            league_id = leagues[0].id

        return league_id

class League_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    league_id = models.IntegerField()

    @classmethod
    def get_choices_by_leagues(cls, leagues):

        league_choices = League_Choices.get_all_items(League_Choices)
        if league_choices.count() > 0:               
            league_choices.delete()
        for league in leagues:
            league_choice = League_Choices(name = league.name, league_id = league.id)
            League_Choices.add_item(League_Choices, league_choice)

    @classmethod
    def make_league_choices(cls):
        league_choices_1 = League_Choices.get_all_items(League_Choices)
        league_choices = []
        for league_choice in league_choices_1:
            league_choices.append((league_choice.league_id, league_choice.name))
        return league_choices


class NFL_Conference(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    league = models.ForeignKey(League, on_delete = models.CASCADE)

    class Meta:
        ordering = ['league']

    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_conference(cls, conference_id, conference_name, conference_league_id):
        return NFL_Conference.objects.filter(id = conference_id, name=conference_name, 
                league_id = conference_league_id)

    @classmethod
    def get_same_conference_in_database(cls, conference_name, conference_league_id):
        return NFL_Conference.objects.filter(name=conference_name, 
            league_id = conference_league_id)

    @classmethod
    def delete_item(cls, conference):
        try:
            #League.delete_conference_divisions(conference.id)
            modelstate = League.delete(conference)
            modelstate = 'Success: ' + conference.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! ' + conference.name + ' was not deleted!'
        return modelstate

    @classmethod
    def get_conference_id_if_needed_and_possible(cls, conferences, conference_id, 
        division_id = 0):

        if conference_id != 0:
            pass
        elif division_id != 0:
            division = NFL_Division.get_item_by_id(NFL_Division, division_id)
            conference_id = division.conference_id 
        elif conferences != []:
            conference_id = conferences[0].id

        return conference_id

class NFL_Conference_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    conference_id = models.IntegerField()

    @classmethod
    def get_choices_by_conferences(cls, conferences):

        conference_choices = NFL_Conference_Choices.get_all_items(NFL_Conference_Choices)
        if conference_choices.count() > 0:               
            conference_choices.delete()
        for conference in conferences:
            conference_choice = NFL_Conference_Choices(name = conference.name, conference_id = conference.id)
            NFL_Conference_Choices.add_item(NFL_Conference_Choices, conference_choice)

    @classmethod
    def make_conference_choices(cls):
        conference_choices_1 = NFL_Conference_Choices.get_all_items(NFL_Conference_Choices)
        conference_choices = []
        for conference_choice in conference_choices_1:
            conference_choices.append((conference_choice.conference_id, conference_choice.name))
        return conference_choices


class NFL_Division(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    conference = models.ForeignKey(NFL_Conference, on_delete = models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_exactly_same_division(cls, division_id, division_name, division_conference_id):
        return NFL_Division.objects.filter(id = division_id, name=division_name, 
                conference_id = division_conference_id)

    @classmethod
    def get_same_division_in_database(cls, division_name, division_conference_id):
        return NFL_Division.objects.filter(name=division_name, 
            conference_id = division_conference_id)

    @classmethod
    def delete_item(cls, division):
        try:
            #League.delete_division_divisions(division.id)
            modelstate = League.delete(division)
            modelstate = 'Success: ' + division.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! ' + division.name + ' was not deleted!'
        return modelstate

class NFL_Division_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    division_id = models.IntegerField()

    @classmethod
    def get_choices_by_divisions(cls, divisions):

        division_choices = NFL_Division_Choices.get_all_items(NFL_Division_Choices)
        if division_choices.count() > 0:               
            division_choices.delete()
        for division in divisions:
            division_choice = NFL_Division_Choices(name = division.name, division_id = division.id)
            NFL_Division_Choices.add_item(NFL_Division_Choices, division_choice)

    @classmethod
    def make_division_choices(cls):
        division_choices_1 = NFL_Division_Choices.get_all_items(NFL_Division_Choices)
        division_choices = []
        for division_choice in division_choices_1:
            division_choices.append((division_choice.division_id, division_choice.name))
        return division_choices


class NFL_TeamCode(models.Model, HelperMixins):

    name = models.CharField(max_length = 20)


class Years(models.Model, HelperMixins):

    year = models.IntegerField()

class Years_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    years_id = models.IntegerField()

    @classmethod
    def get_choices_by_yearss(cls, yearss):

        years_choices = Years_Choices.get_all_items(Years_Choices)
        if years_choices.count() > 0:               
            years_choices.delete()
        for years in yearss:
            years_choice = Years_Choices(name = years.name, years_id = years.id)
            Years_Choices.add_item(Years_Choices, years_choice)

    @classmethod
    def make_years_choices(cls):
        years_choices_1 = Years_Choices.get_all_items(Years_Choices)
        years_choices = []
        for years_choice in years_choices_1:
            years_choices.append((years_choice.years_id, years_choice.name))
        return years_choices


class NFL_Team(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    team_abbrv = models.CharField(max_length = 10)
    label_filename = models.CharField(max_length = 50)
    icon_filename = models.CharField(max_length = 50)

    start_year = models.ForeignKey(Years, on_delete = models.DO_NOTHING, related_name = 'start_year')
    end_year = models.ForeignKey(Years, on_delete = models.DO_NOTHING, null = True, related_name = 'end_year')
    division = models.ForeignKey(NFL_Division, on_delete = models.CASCADE)
    code = models.ForeignKey(NFL_TeamCode, on_delete = models.DO_NOTHING)

    class Meta:
        ordering = ['division']

    def __str__(self):
        return self.name

class NFL_Team_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    nfl_team_id = models.IntegerField()

    @classmethod
    def get_choices_by_nfl_teams(cls, nfl_teams):

        nfl_team_choices = NFL_Team_Choices.get_all_items(NFL_Team_Choices)
        if nfl_team_choices.count() > 0:               
            nfl_team_choices.delete()
        for nfl_team in nfl_teams:
            nfl_team_choice = NFL_Team_Choices(name = nfl_team.name, nfl_team_id = nfl_team.id)
            NFL_Team_Choices.add_item(NFL_Team_Choices, nfl_team_choice)

    @classmethod
    def make_nfl_team_choices(cls):
        nfl_team_choices_1 = NFL_Team_Choices.get_all_items(NFL_Team_Choices)
        nfl_team_choices = []
        for nfl_team_choice in nfl_team_choices_1:
            nfl_team_choices.append((nfl_team_choice.nfl_team_id, nfl_team_choice.name))
        return nfl_team_choices


class NFL_Season(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    league = models.ForeignKey(League, on_delete = models.CASCADE)
    year = models.ForeignKey(Years, on_delete = models.DO_NOTHING)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return self.name

class NFL_Season_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    nfl_season_id = models.IntegerField()

    @classmethod
    def get_choices_by_nfl_seasons(cls, nfl_seasons):

        nfl_season_choices = NFL_Season_Choices.get_all_items(NFL_Season_Choices)
        if nfl_season_choices.count() > 0:               
            nfl_season_choices.delete()
        for nfl_season in nfl_seasons:
            nfl_season_choice = NFL_Season_Choices(name = nfl_season.name, nfl_season_id = nfl_season.id)
            NFL_Season_Choices.add_item(NFL_Season_Choices, nfl_season_choice)

    @classmethod
    def make_nfl_season_choices(cls):
        nfl_season_choices_1 = NFL_Season_Choices.get_all_items(NFL_Season_Choices)
        nfl_season_choices = []
        for nfl_season_choice in nfl_season_choices_1:
            nfl_season_choices.append((nfl_season_choice.nfl_season_id, nfl_season_choice.name))
        return nfl_season_choices


class NFL_SeasonType(models.Model, HelperMixins):
  
    name = models.CharField(max_length = 50)
    league = models.ForeignKey(League, on_delete = models.DO_NOTHING)

class NFL_SeasonType_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    nfl_seasontype_id = models.IntegerField()

    @classmethod
    def get_choices_by_nfl_seasontypes(cls, nfl_seasontypes):

        nfl_seasontype_choices = NFL_SeasonType_Choices.get_all_items(NFL_SeasonType_Choices)
        if nfl_seasontype_choices.count() > 0:               
            nfl_seasontype_choices.delete()
        for nfl_seasontype in nfl_seasontypes:
            nfl_seasontype_choice = NFL_SeasonType_Choices(name = nfl_seasontype.name, nfl_seasontype_id = nfl_seasontype.id)
            NFL_SeasonType_Choices.add_item(NFL_SeasonType_Choices, nfl_seasontype_choice)

    @classmethod
    def make_nfl_seasontype_choices(cls):
        nfl_seasontype_choices_1 = NFL_SeasonType_Choices.get_all_items(NFL_SeasonType_Choices)
        nfl_seasontype_choices = []
        for nfl_seasontype_choice in nfl_seasontype_choices_1:
            nfl_seasontype_choices.append((nfl_seasontype_choice.nfl_seasontype_id, nfl_seasontype_choice.name))
        return nfl_seasontype_choices


class NFL_Schedule(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_custom = models.BooleanField(default = False)

    season = models.ForeignKey(NFL_Season, on_delete = models.CASCADE)
    schedule_type = models.ForeignKey(NFL_SeasonType, on_delete = models.DO_NOTHING)
    cronjob_id = models.IntegerField(null = True)

    class Meta:
        ordering = ['-season']

    def __str__(self):
        return self.name

class NFL_Schedule_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    nfl_schedule_id = models.IntegerField()

    @classmethod
    def get_choices_by_nfl_schedules(cls, nfl_schedules):

        nfl_schedule_choices = NFL_Schedule_Choices.get_all_items(NFL_Schedule_Choices)
        if nfl_schedule_choices.count() > 0:               
            nfl_schedule_choices.delete()
        for nfl_schedule in nfl_schedules:
            nfl_schedule_choice = NFL_Schedule_Choices(name = nfl_schedule.name, nfl_schedule_id = nfl_schedule.id)
            NFL_Schedule_Choices.add_item(NFL_Schedule_Choices, nfl_schedule_choice)

    @classmethod
    def make_nfl_schedule_choices(cls):
        nfl_schedule_choices_1 = NFL_Schedule_Choices.get_all_items(NFL_Schedule_Choices)
        nfl_schedule_choices = []
        for nfl_schedule_choice in nfl_schedule_choices_1:
            nfl_schedule_choices.append((nfl_schedule_choice.nfl_schedule_id, nfl_schedule_choice.name))
        return nfl_schedule_choices


class CronJob (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    cronjobtype = models.ForeignKey(CronJobType, on_delete=models.CASCADE)
    nfl_schedule = models.ForeignKey(NFL_Schedule, on_delete = models.DO_NOTHING, null = True)
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

class CronJob_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    cronjob_id = models.IntegerField()

    @classmethod
    def get_cronjob_choices(cls, cronjobs):

        cronjob_choices = CronJob_Choices.get_all_items(CronJob_Choices)
        if cronjob_choices.count() > 0:               
            cronjob_choices.delete()

        cronjob_choice = CronJob_Choices(name = 'none', cronjob_id = -1)
        CronJob_Choices.add_item(CronJob_Choices, cronjob_choice)
            
        for cronjob in cronjobs:
            cronjob_choice = CronJob_Choices(name = cronjob.name, cronjob_id = cronjob.id)
            CronJob_Choices.add_item(CronJob_Choices, cronjob_choice)


    @classmethod
    def make_cronjob_choices(cls):
        cronjob_choices_1 = CronJob_Choices.get_all_items(CronJob_Choices)
        cronjob_choices = []
        for cronjob_choice in cronjob_choices_1:
            cronjob_choices.append((cronjob_choice.cronjob_id, cronjob_choice.name))
        return cronjob_choices


class Pool (models.Model, HelperMixins):

    name = models.CharField(max_length = 50)

    poolgroup = models.ForeignKey(PoolGroup, on_delete = models.CASCADE)
    poolowner = models.ForeignKey(PoolOwner, on_delete = models.DO_NOTHING)
    pooltype = models.ForeignKey(PoolType, on_delete = models.DO_NOTHING)
    cronjob = models.ForeignKey(CronJob, on_delete = models.DO_NOTHING, null = True)

    def __str__(self):
        return self.name

    @classmethod
    def get_items_by_groupowner_id(cls, model_cls, model_groupowner_id):
        pools = []
        poolgroups = PoolGroup.get_items_by_groupowner_id(PoolGroup, model_groupowner_id)
        for poolgroup in poolgroups:
            poolgroup_pools = Pool.get_items_by_poolgroup_id(Pool, poolgroup.id)
            for pool in poolgroup_pools:
                pools.append(pool)
        return pools

    @classmethod
    def get_same_pool_in_database(cls, pool_name, pool_id = 0):
        same_pool = None
        try:
            same_pool = Pool.objects.get(name=pool_name)
        except:
            pass
        if same_pool != None:
            if same_pool.id == pool_id and pool_id != 0:
                same_pool = None
        return same_pool

    @classmethod
    def get_exactly_same_pool(cls, id, name, cronjob_id, pooltype_id, poolgroup_id, poolowner_id):
        exactly_same_pool = None
        try:
            exactly_same_pool = Pool.objects.filter(id = id, name = name, cronjob_id = cronjob_id, 
                pooltype_id = pooltype_id, poolgroup_id = poolgroup_id, poolowner_id = poolowner_id)
        except:
            pass
        return exactly_same_pool

    @classmethod
    def filter_pools(cls, pools, groupowner_id = 0, poolgroup_id = 0, poolowner_id = 0):

        filtered_pools = []

        if poolowner_id != 0:
            for pool in pools:
                if pool.poolowner_id == poolowner_id:
                    filtered_pools.append(pool)
        '''
        elif poolgroup_id != 0:
            for pool in pools:
                if pool.poolgroup_id == poolgroup_id:
                    filtered_pools.append(pool)
        elif groupowner_id != 0:
            for pool in pools:
                if pool.poolgroup.groupowner_id == groupowner_id:
                    filtered_pools.append(pool)
        '''
        return filtered_pools

    @classmethod
    def get_pools_by_poolowners(cls, poolowners):

        pools = []
        for poolowner in poolowners:
            poolowner_pools = Pool.get_items_by_poolowner_id(Pool, poolowner.id)
            for poolowner_pool in poolowner_pools:
                pools.append(poolowner_pool)
        return pools

    @classmethod
    def get_pools_by_poolgroups(cls, poolgroups):

        pools = []
        for poolgroup in poolgroups:
            poolgroup_pools = Pool.get_items_by_poolgroup_id(Pool, poolgroup.id)
            for poolgroup_pool in poolgroup_pools:
                pools.append(poolgroup_pool)
        return pools

    @classmethod
    def get_pools_by_groupowners(cls, groupowners):

        pools = []
        for groupowner in groupowners:
            groupowner_pools = Pool.get_items_by_groupowner_id(Pool, groupowner.id)
            for groupowner_pool in groupowner_pools:
                pools.append(groupowner_pool)
        return pools

    @classmethod
    def transfer_pool_ownership(cls, pools, new_poolowner_id, modelstate):
        error = None
        for pool in pools:
            pool.poolowner_id = new_poolowner_id
            modelstate = PoolGroup.edit_item(Pool, pool)
            if modelstate.split(':')[0] != 'Success':
                error = 'Error'
        if error == None:
            return 'Success: Pool ownership was transfered'
        else:
            return 'Error: Database Error must be investigated'

    @classmethod
    def transfer_pool_ownership_2(cls, pool, new_poolowner_id, modelstate):
        error = None

        pool.poolowner_id = new_poolowner_id
        modelstate = PoolGroup.edit_item(Pool, pool)
        if modelstate.split(':')[0] != 'Success':
            error = 'Error'

        if error == None:
            return 'Success: Pool ownership was transfered'
        else:
            return 'Error: Database Error must be investigated'

    @classmethod
    def delete_poolowner_pools(cls, poolowner_id):
        
        poolowner_pools = Pool.get_items_by_poolowner_id(Pool, poolowner_id)
        for poolowner_pool in poolowner_pools:
            Pool.delete_item(Pool, poolowner_pool)

class Pool_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    pool_id = models.IntegerField()

    @classmethod
    def get_choices_by_pools(cls, pools):

        pool_choices = Pool_Choices.get_all_items(Pool_Choices)
        if pool_choices.count() > 0:               
            pool_choices.delete()
        for pool in pools:
            pool_choice = Pool_Choices(name = pool.name, pool_id = pool.id)
            Pool_Choices.add_item(Pool_Choices, pool_choice)

    @classmethod
    def make_pool_choices(cls):
        pool_choices_1 = Pool_Choices.get_all_items(Pool_Choices)
        pool_choices = []
        for pool_choice in pool_choices_1:
            pool_choices.append((pool_choice.pool_id, pool_choice.name))
        return pool_choices


class NFL_TimePeriod(models.Model, HelperMixins):

    name = models.CharField(max_length = 10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    schedule = models.ForeignKey(NFL_Schedule, on_delete = models.CASCADE)

    class Meta:
        ordering = ['schedule']

    def __str__(self):
        return self.name

class NFL_TimePeriod_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    nfl_timeperiod_id = models.IntegerField()

    @classmethod
    def get_choices_by_nfl_timeperiods(cls, nfl_timeperiods):

        nfl_timeperiod_choices = NFL_TimePeriod_Choices.get_all_items(NFL_TimePeriod_Choices)
        if nfl_timeperiod_choices.count() > 0:               
            nfl_timeperiod_choices.delete()
        for nfl_timeperiod in nfl_timeperiods:
            nfl_timeperiod_choice = NFL_TimePeriod_Choices(name = nfl_timeperiod.name, nfl_timeperiod_id = nfl_timeperiod.id)
            NFL_TimePeriod_Choices.add_item(NFL_TimePeriod_Choices, nfl_timeperiod_choice)

    @classmethod
    def make_nfl_timeperiod_choices(cls):
        nfl_timeperiod_choices_1 = NFL_TimePeriod_Choices.get_all_items(NFL_TimePeriod_Choices)
        nfl_timeperiod_choices = []
        for nfl_timeperiod_choice in nfl_timeperiod_choices_1:
            nfl_timeperiod_choices.append((nfl_timeperiod_choice.nfl_timeperiod_id, nfl_timeperiod_choice.name))
        return nfl_timeperiod_choices


class NFL_Game(models.Model, HelperMixins):

    nfl_gamekey = models.CharField(max_length = 15)
    nfl_eid = models.CharField(max_length = 15)
    nfl_wknum = models.IntegerField()
    nfl_seasontype = models.CharField(max_length = 10)
    nfl_hometeam = models.ForeignKey(NFL_Team, on_delete = models.DO_NOTHING, null = True, related_name = 'nfl_hometeam')
    nfl_hometeam_abbrv = models.CharField(max_length = 10)
    nfl_awayteam = models.ForeignKey(NFL_Team, on_delete = models.DO_NOTHING, null = True, related_name = 'nfl_awayteam')
    nfl_awayteam_abbrv = models.CharField(max_length = 10)
    nfl_merdian = models.CharField(max_length = 10)
    nfl_year = models.IntegerField()
    nfl_month = models.IntegerField()
    nfl_day = models.IntegerField()
    nfl_wkday = models.CharField(max_length = 10)
    nfl_time = models.CharField(max_length = 10)
    start_time = models.DateTimeField()
    timeperiod = models.ForeignKey(NFL_TimePeriod, on_delete = models.DO_NOTHING, null = True)
    data_error = models.CharField(max_length = 10, null = True)

    class Meta:
        ordering = ['nfl_gamekey']

    def __str__(self):
        return self.name

class NFL_Game_Choices(models.Model, HelperMixins):

    name = models.CharField(max_length = 50)
    nfl_game_id = models.IntegerField()

    @classmethod
    def get_choices_by_nfl_games(cls, nfl_games):

        nfl_game_choices = NFL_Game_Choices.get_all_items(NFL_Game_Choices)
        if nfl_game_choices.count() > 0:               
            nfl_game_choices.delete()
        for nfl_game in nfl_games:
            nfl_game_choice = NFL_Game_Choices(name = nfl_game.name, nfl_game_id = nfl_game.id)
            NFL_Game_Choices.add_item(NFL_Game_Choices, nfl_game_choice)

    @classmethod
    def make_nfl_game_choices(cls):
        nfl_game_choices_1 = NFL_Game_Choices.get_all_items(NFL_Game_Choices)
        nfl_game_choices = []
        for nfl_game_choice in nfl_game_choices_1:
            nfl_game_choices.append((nfl_game_choice.nfl_game_id, nfl_game_choice.name))
        return nfl_game_choices
