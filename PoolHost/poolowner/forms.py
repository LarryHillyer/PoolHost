from django import forms
from django.forms import ModelForm
from django.db import models

from app.models import PoolOwner
from app.models import GroupOwner_Choices, PoolGroup_Choices, PoolOwner_Choices

class PoolOwnerForm_Create(ModelForm):
    
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

class PoolOwnerForm_Transfer(ModelForm):


    
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
        model = PoolOwner
        fields = ['name']
