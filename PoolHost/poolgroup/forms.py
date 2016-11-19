from django import forms
from django.forms import ModelForm
from django.db import models
from app.models import GroupOwner, PoolGroup

class PoolGroupForm(ModelForm):
    groupowners = GroupOwner.get_all_items(GroupOwner)
    groupowner_choices = []
    for groupowner in groupowners:
        groupowner_choice = (groupowner.id, groupowner.name)
        groupowner_choices.append(groupowner_choice)
    
    name = forms.CharField(max_length = 100,
                            widget = forms.TextInput({
                                    'class':'form-control',
                                    'placeholder': 'Enter Pool Group Name'}))

    groupowner_id = forms.ChoiceField(choices = groupowner_choices,
                            widget = forms.Select({'class':'form-control'}))
    class Meta:
        model = PoolGroup
        fields = ['name', 'groupowner_id']