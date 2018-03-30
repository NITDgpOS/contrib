import requests

from django import forms
from django.utils.translation import gettext as _

from core.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        url = 'https://api.github.com/users/{}'.format(username)
        r = requests.get(url)
        if r.status_code != 200:
            raise forms.ValidationError(
                _("No github account found related to this username"),
                code='not_found'
            )
        cleaned_data['name'] = r.json().get('name')

    class Meta:
        model = User
        fields = ('username',)
