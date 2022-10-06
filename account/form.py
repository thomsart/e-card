from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  
    class Meta:  
        model = User  
        fields = ['email', 'password']


class LoginForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)  
    class Meta:  
        model = User  
        fields = ['email', 'password']


class ClientForm(forms.Form):

    first_name = forms.CharField(label='prenom', max_length=20)
    last_name = forms.CharField(label='nom', max_length=20)
    email = forms.EmailField(label='email', max_length=254)
