from django import forms


# Create your form here.

class ClientForm(forms.Form):

    first_name = forms.CharField(label='prenom', max_length=20)
    last_name = forms.CharField(label='nom', max_length=20)
    email = forms.EmailField(label='email', max_length=254)
