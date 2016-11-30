from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import GroupOwner, GroupOwner_Choices

class GroupOwnerForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Group Owner User Name'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = GroupOwner
        fields = ['name']

class GroupOwnerForm_Transfer(ModelForm):
    
    name = forms.CharField(max_length = 100, required = False,
                        widget = forms.TextInput({
                                'class':'form-control',
                                'disabled': 'disabled'}))

    new_groupowner_id = forms.ChoiceField(choices = GroupOwner_Choices.make_groupowner_choices,
                                            widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = GroupOwner
        fields = ['name']