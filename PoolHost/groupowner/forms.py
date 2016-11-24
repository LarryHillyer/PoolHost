from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import GroupOwner

class GroupOwnerForm(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Group Owner User Name'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = GroupOwner
        fields = ['name']