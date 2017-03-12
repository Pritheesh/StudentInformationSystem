from django import forms
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.validators import validate_email

from InfoSystem.models import Student, Parent
from .models import CustomUser

class UserForm(forms.Form):
    email = forms.EmailField()
    mobile =forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'mobile')


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
    isstudent = forms.NullBooleanField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Username can only contain alphanumeric characters")
        try:
            CustomUser.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError("Username already exists")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            return email
        except:
            raise forms.ValidationError("Enter correct Email")

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if 'isstudent' in self.data:
        #     is_student = True
        # else:
        #     is_student = False
        # if is_student is True:
            try:
                stud = Student.objects.get(mobile=mobile)
            except:
                raise forms.ValidationError("User with given mobile number doesn't exist")
            if stud.is_registered is True:
                raise forms.ValidationError("Student with given mobile number already exists")
            return mobile
        else:
            try:
                par = Parent.objects.get(mobile=mobile)
            except:
                raise forms.ValidationError("User with given mobile number doesn't exist")
            if par.is_registered is True:
                raise forms.ValidationError("Parent with given mobile number already exists")
            return mobile


    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError("Passwords do not match")

    # def clean(self):
    #     self.clean_password2()
    #     self.clean_mobile()
    #     self.clean_email()
    #     self.clean_username()

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        user = authenticate(username = self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is None:
            raise forms.ValidationError("Invalid username or password. Please try again!")
