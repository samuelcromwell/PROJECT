from collections.abc import Mapping
from typing import Any
from users.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
import datetime

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class':'input','type':'date','placeholder':'Date of Birth'}, format=['%d-%m-%Y']))

    class Meta:
        model = get_user_model() 
        fields = ['username','first_name', 'last_name', 'date_of_birth', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'input','type':'text','placeholder':'Username'})
        self.fields['first_name'].widget.attrs.update({'class':'input','type':'text','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class':'input','type':'text','placeholder':'Last Name'})
        self.fields['email'].widget.attrs.update({'class':'input','type':'text','placeholder':'Email address'})
        self.fields['date_of_birth'].widget.attrs.update({'class':'input','type':'date','placeholder':'Date of Birth'}) 
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password 1'})    
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password 2'})    

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > datetime.date.today() - datetime.timedelta(days=18*365):
            raise forms.ValidationError('You must be at least 18 years old to register.')
        return date_of_birth
    
class UserLoginForm(forms.ModelForm):    
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'input','type':'text','placeholder':'Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'})
