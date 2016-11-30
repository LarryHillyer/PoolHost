from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import PoolType

class PoolTypeForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100, label = 'Pool Type',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Type'}))
    class Meta:
        model = PoolType
        fields = ['name']

class PoolTypeForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput())    

    name = forms.CharField(max_length = 100, label = 'Pool Type',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Type'}))
    class Meta:
        model = PoolType
        fields = ['id', 'name']