from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class EditProfileForm(UserChangeForm):
    password = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'      
        )

