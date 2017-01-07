from django import forms


class NameForm(forms.Form):
    name = forms.CharField(label="Your Roll Num", max_length=128)