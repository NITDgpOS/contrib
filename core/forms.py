import requests

from django import forms
from django.utils.translation import gettext as _

from core.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        url = 'https://api.github.com/users/{}'.format(username)
        r = requests.get(url)
        if r.status_code != 200:
            raise forms.ValidationError(
                _("No github account found related to this username"),
                code='not_found'
            )
        return username

    class Meta:
        model = User
        fields = ('username',)
