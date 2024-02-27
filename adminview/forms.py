from django import forms

class UserRegisterForm:
    email = forms.EmailField()
    
    class Meta:
        
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'input','type':'text','placeholder':'Username'})
        self.fields['first_name'].widget.attrs.update({'class':'input','type':'text','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class':'input','type':'text','placeholder':'Last Name'})
        self.fields['email'].widget.attrs.update({'class':'input','type':'text','placeholder':'Email address'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password 1'})    
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password 2'})    

   