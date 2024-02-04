from collections.abc import Mapping
from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.update({'class':'input','type':'text','placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'class':'input','type':'text','placeholder':'Email address'})
        self.fields['password'].widget.attrs.update({'class':'input','type':'password','placeholder':'Password'})
