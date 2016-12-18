from django import forms
from django.forms import ModelForm
from django.db import models

from app.models import NFL_Conference
from app.models import Sport_Choices, League_Choices, NFL_Conference_Choices

class NFL_ConferenceForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Conference Name'}))

    class Meta:
        model = NFL_Conference
        fields = ['name']

class NFL_ConferenceForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput())
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Conference Name'}))

    class Meta:
        model = NFL_Conference
        fields = ['id', 'name']
