from django import forms

from core.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username',)
