from distutils.command.upload import upload
from django import forms


# Create your form here.

class CardForm(forms.Form):

    profession = forms.CharField(label='profession', max_length=20)
    phone = forms.CharField(label='phone', max_length=15)
    # email = forms.EmailField(label='email', max_length=254)
    description = forms.CharField(label='description', max_length=198, required=False, widget=forms.Textarea)
    photo = forms.ImageField(max_length=300, allow_empty_file=True, required=True, label="photo")
