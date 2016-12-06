from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import PoolGroup, GroupOwner_Choices, GroupOwner

class PoolGroupForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))

    groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = PoolGroup
        fields = ['name', 'groupowner_id']

class PoolGroupForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput({}))
   
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))
    
    groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = PoolGroup
        fields = ['id', 'name', 'groupowner_id']

class PoolGroupForm_Transfer(ModelForm):

    name = forms.CharField(max_length = 100, required = False,
                        widget = forms.TextInput({
                                'class':'form-control',
                                'disabled': 'disabled'}))

    groupowner_name=forms.CharField(max_length = 100, required = False,
                        widget = forms.TextInput({
                                'class': 'form-control',
                                'disabled': 'disabled',}))

    new_groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                                            widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = PoolGroup
        fields = ['name']


