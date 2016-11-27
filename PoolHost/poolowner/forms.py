from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import PoolOwner
from app.models import GroupOwner_Choices, PoolGroup_Choices

class PoolOwnerForm_SuperUser_Create(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Owner Name'}))

    poolgroup_id = forms.ChoiceField(choices = PoolGroup_Choices.make_poolgroup_choices,
                            widget = forms.Select({'class':'form-control'}))

    groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                            widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = PoolOwner
        fields = ['name', 'poolgroup_id']

class PoolOwnerForm_SuperUser_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput({}))
   
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))

    poolgroup_id = forms.ChoiceField(choices = PoolGroup_Choices.make_poolgroup_choices,
                            widget = forms.Select({'class':'form-control'}))
    
    groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                            widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = PoolOwner
        fields = ['id', 'name', 'poolgroup_id']

class PoolOwnerForm_SuperUser_Transfer(ModelForm):

    
    poolowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                                            widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = PoolOwner
        fields = ['poolowner_id']


class PoolOwnerForm_GroupOwner_Create(ModelForm):

   
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))

    poolgroup_id = forms.ChoiceField(choices = PoolGroup_Choices.make_poolgroup_choices,
                            widget = forms.Select({'class':'form-control'}))    
    
    groupowner_id = forms.IntegerField(widget = forms.HiddenInput())
    
    filter = forms.IntegerField(widget = forms.HiddenInput())
                        
    class Meta:
        model = PoolOwner
        fields = [ 'name', 'poolgroup_id']

class PoolOwnerForm_GroupOwner_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput({}))
   
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))

    poolgroup_id = forms.ChoiceField(choices = PoolGroup_Choices.make_poolgroup_choices,
                            widget = forms.Select({'class':'form-control'}))
    
    groupowner_id = forms.IntegerField(widget = forms.HiddenInput())

    filter = forms.IntegerField(widget = forms.HiddenInput())
                        
    class Meta:
        model = PoolOwner
        fields = ['id', 'name', 'poolgroup_id']
