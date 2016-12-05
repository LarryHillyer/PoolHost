from django import forms
from django.forms import ModelForm
from django.db import models

from app.models import Pool
from app.models import GroupOwner_Choices, PoolGroup_Choices, PoolOwner_Choices
from app.models import CronJob_Choices, PoolType_Choices

class PoolForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Name'}))

    cronjob_id = forms.ChoiceField(choices = CronJob_Choices.make_cronjob_choices,
                            widget = forms.Select({'class':'form-control'}))

    pooltype_id = forms.ChoiceField(choices = PoolType_Choices.make_pooltype_choices,
                            widget = forms.Select({'class':'form-control'}))

    groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    poolgroup_id = forms.ChoiceField(choices = PoolGroup_Choices.make_poolgroup_choices,
                            widget = forms.Select({'class':'form-control'}))

    poolowner_id = forms.ChoiceField(choices = PoolOwner_Choices.make_poolowner_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = Pool
        fields = ['name', 'poolgroup_id', 'poolowner_id', 'cronjob_id', 'pooltype_id']

class PoolForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput())
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Name'}))

    cronjob_id = forms.ChoiceField(choices = CronJob_Choices.make_cronjob_choices,
                            widget = forms.Select({'class':'form-control'}))

    pooltype_id = forms.ChoiceField(choices = PoolType_Choices.make_pooltype_choices,
                            widget = forms.Select({'class':'form-control'}))

    groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    poolgroup_id = forms.ChoiceField(choices = PoolGroup_Choices.make_poolgroup_choices,
                            widget = forms.Select({'class':'form-control'}))

    poolowner_id = forms.ChoiceField(choices = PoolOwner_Choices.make_poolowner_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = Pool
        fields = ['id', 'name', 'poolgroup_id', 'poolowner_id', 'cronjob_id', 'pooltype_id']


class PoolForm_Transfer(ModelForm):


    
    name = forms.CharField(max_length = 100, required = False,
                        widget = forms.TextInput({
                                'class':'form-control',
                                'disabled': 'disabled'}))

    poolgroup_name=forms.CharField(max_length = 100, required = False,
                        widget = forms.TextInput({
                                'class': 'form-control',
                                'disabled': 'disabled',}))

    new_poolowner_id = forms.ChoiceField(choices = PoolOwner_Choices.make_poolowner_choices,
                                            widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = Pool
        fields = ['name']
