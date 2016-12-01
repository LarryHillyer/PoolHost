from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import CronJob, CronJobType_Choices

class CronJobForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100, label = 'Cron Job',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Cron Job'}))

    cronjobtype_id = forms.ChoiceField(choices = CronJobType_Choices.make_cronjobtype_choices,
                                        widget = forms.Select({
                                                'class':'form-control'}))

    class Meta:
        model = CronJob
        fields = ['name', 'cronjobtype_id']

class CronJobForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput())    

    name = forms.CharField(max_length = 100, label = 'Cron Job',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Cron Job'}))

    cronjobtype_id = forms.ChoiceField(choices = CronJobType_Choices.make_cronjobtype_choices,
                                        widget = forms.Select({
                                                'class':'form-control'}))

    class Meta:
        model = CronJob
        fields = ['id', 'name', 'cronjobtype_id']