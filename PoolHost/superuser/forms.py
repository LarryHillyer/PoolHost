from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import SuperUser

class SuperUserForm(ModelForm):
    
    name = forms.CharField(max_length = 100, label = 'Super User Name',
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Superuser User Name'}))
    class Meta:
        model = SuperUser
        fields = ['name']