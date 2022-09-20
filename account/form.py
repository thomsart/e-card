from django.contrib.auth.models import User
from django import forms


# Create your form here.

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']
        # widgets = {'username':forms.HiddenInput()}

    def clean_username(self):
        return self.cleaned_data.get('email')