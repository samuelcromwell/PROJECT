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
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'input','type':'text','placeholder':'Username'})
        self.fields['first_name'].widget.attrs.update({'class':'input','type':'text','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class':'input','type':'text','placeholder':'Last Name'})
        self.fields['email'].widget.attrs.update({'class':'input','type':'text','placeholder':'Email address'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password 1'})    
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password 2'})    

class UserLoginForm(forms.ModelForm):    
    
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'input','type':'text','placeholder':'Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'})

        