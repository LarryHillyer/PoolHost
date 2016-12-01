from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import CronJobType

class CronJobTypeForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100, label = 'Cron Job Type',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Cron Job Type'}))
    class Meta:
        model = CronJobType
        fields = ['name']

class CronJobTypeForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput())    

    name = forms.CharField(max_length = 100, label = 'Cron Job Type',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Cron Job Type'}))
    class Meta:
        model = CronJobType
        fields = ['id', 'name']