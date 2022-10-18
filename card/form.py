from distutils.command.upload import upload
from django import forms


class CardForm(forms.Form):

    title = forms.CharField(label='profession ou passion', max_length=25, required=False)
    description = forms.CharField(label='description', widget=forms.Textarea, max_length=135, required=False)
    website = forms.URLField(label='site web', required=False)
    photo = forms.ImageField(label="photo", max_length=300, allow_empty_file=True, required=False)
