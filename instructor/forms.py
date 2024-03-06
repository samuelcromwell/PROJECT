from django import forms
from .models import Progress

class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['progress_percentage', 'trainee']
