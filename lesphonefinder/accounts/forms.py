# -*- coding: utf-8 -*-


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy
 
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label=ugettext_lazy("First Name"), required=True, min_length=5,max_length=30)
    last_name = forms.CharField(label=ugettext_lazy("Last Name"), required=True, min_length=5, max_length=30)
     
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
 
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
        
        return user
