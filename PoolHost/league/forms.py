from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import League, Sport_Choices, Sport

class LeagueForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter League Name'}))

    sport_id = forms.ChoiceField(choices = Sport_Choices.make_sport_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = League
        fields = ['name', 'sport_id']

class LeagueForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput({}))
   
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter League Name'}))
    
    sport_id = forms.ChoiceField(choices = Sport_Choices.make_sport_choices,
                            widget = forms.Select({'class':'form-control'}),
                            required = False)

    filter = forms.IntegerField(widget = forms.HiddenInput())

    class Meta:
        model = League
        fields = ['id', 'name', 'sport_id']
