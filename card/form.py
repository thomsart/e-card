from django import forms


# Create your form here.

class CardForm(forms.Form):

    profession = forms.CharField(label='profession', max_length=20)
    phone = forms.CharField(label='phone', max_length=15)
    email = forms.EmailField(label='email', max_length=254)
