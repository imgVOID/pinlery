from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField(label='Target board username', max_length=26)