from django import forms
from django.forms import ModelForm
from django.db import models

from app.models import NFL_Division
from app.models import NFL_Conference_Choices

class NFL_DivisionForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Division Name'}))

    conference_id = forms.ChoiceField(choices = NFL_Conference_Choices.make_conference_choices,
                                        widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = NFL_Division
        fields = ['name', 'conference_id']

class NFL_DivisionForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput())
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Division Name'}))

    conference_id = forms.ChoiceField(choices = NFL_Conference_Choices.make_conference_choices,
                                        widget = forms.Select({'class':'form-control'}))

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = NFL_Division
        fields = ['id', 'name', 'conference_id']
