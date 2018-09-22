from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from .models import Profile


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
