from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import Sport

class SportForm_Create(ModelForm):
    
    name = forms.CharField(max_length = 100, label = 'Sport',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Sport'}))

    class Meta:
        model = Sport
        fields = ['name']

class SportForm_Edit(ModelForm):

    id = forms.IntegerField(widget = forms.HiddenInput())    

    name = forms.CharField(max_length = 100, label = 'Sport',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Sport'}))


    class Meta:
        model = Sport
        fields = ['id', 'name']