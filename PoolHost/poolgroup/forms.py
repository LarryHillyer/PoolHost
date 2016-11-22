from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import SiteUser, GroupOwner, PoolGroup, GroupOwner_Choices

class PoolGroupForm(ModelForm):

    groupowner_choices_1 = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
    groupowner_choices = []
    for groupowner_choice in groupowner_choices_1:
        groupowner_choices.append((groupowner_choice.groupowner_id, groupowner_choice.name))
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))

    groupowner_id = forms.ChoiceField(choices = groupowner_choices,
                            widget = forms.Select({'class':'form-control'}))
    class Meta:
        model = PoolGroup
        fields = ['name', 'groupowner_id']

class PoolGroupForm_SuperUser_Edit(ModelForm):

    groupowner_choices_1 = GroupOwner_Choices.get_all_items(GroupOwner_Choices)
    groupowner_choices = []
    for groupowner_choice in groupowner_choices_1:
        groupowner_choices.append((groupowner_choice.groupowner_id, groupowner_choice.name))

    id = forms.IntegerField(widget = forms.HiddenInput({}))
   
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))
    
    groupowner_id = forms.ChoiceField(choices = groupowner_choices,
                            widget = forms.Select({'class':'form-control'}))
    class Meta:
        model = PoolGroup
        fields = ['id', 'name', 'groupowner_id']

class PoolGroupForm_GroupOwner_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput({}))
   
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))
    
    groupowner_id = forms.IntegerField(widget = forms.HiddenInput({}))
                            
    class Meta:
        model = PoolGroup
        fields = ['id', 'name', 'groupowner_id']