from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Parent

class NameForm(forms.Form):
    name = forms.CharField(label="Your Roll Num", max_length=128)
