from django import forms
import re, string, random

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.validators import validate_email
from django.forms.models import ModelForm

from InfoSystem.models import Student, Parent, ExamInfo
from .models import CustomUser



class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    sheets = forms.CharField()
    start = forms.CharField()

class ResultsForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    is_supple = forms.CharField(label='0 for main, 1 for supple')
    year_of_calendar = forms.CharField()
    month_of_year = forms.CharField()
    semester = forms.CharField()
    semester_roman = forms.CharField()
    year_of_pursue = forms.CharField()
    year_of_pursue_roman = forms.CharField()
    sheets = forms.CharField()
    start = forms.CharField()
    batch = forms.CharField()

    # class Meta:
    #     fields = ('year_of_pursue', 'semester', 'year_of_pursue_roman', 'semester_roman', 'year_of_calendar',
    #               'month_of_year', 'is_supple')
    # pass

class UserForm(forms.Form):
    email = forms.EmailField()
    mobile =forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'mobile', 'is_student')


#for token
class UserRegistrationForm2(UserCreationForm):
    mobile = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'mobile', 'is_student', 'password1', 'password2')

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
        except forms.ValidationError as e:
            raise forms.ValidationError(e.messages)
        if CustomUser.objects.filter(email=email).count() != 0:
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if 'isstudent' in self.data:
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
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            else:
                try:
                    validate_password(password1)
                    return password1
                except exceptions.ValidationError as e:
                #     errors['password1'] = list(e.messages)
                #
                # if errors:
                    raise forms.ValidationError(e.messages)

    def save(self, commit=True):
        user =  super(UserRegistrationForm2, self).save(commit=False)
        user.mobile = self.cleaned_data['mobile']
        user.set_password(self.cleaned_data['password1'])
        if 'isstudent' in self.data:
            user.is_student = True
        else:
            user.is_student = False
        if commit:
            user.save()

        return user


#for email
class UserRegistrationForm(ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'mobile', 'is_student', 'password', 'password2')

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
        except forms.ValidationError as e:
            raise forms.ValidationError(e.messages)
        if CustomUser.objects.filter(email=email).count() != 0:
            raise forms.ValidationError("This email has already been used for registration.")
        return email

    # def clean_mobile(self):
    #     mobile = self.cleaned_data['mobile']
    #     if 'isstudent' in self.data:
    #         try:
    #             stud = Student.objects.get(mobile=mobile)
    #         except:
    #             raise forms.ValidationError("User with given mobile number doesn't exist")
    #         if stud.is_registered is True:
    #             raise forms.ValidationError("Student with given mobile number already exists")
    #         return mobile
    #     else:
    #         try:
    #             par = Parent.objects.get(mobile=mobile)
    #         except:
    #             raise forms.ValidationError("User with given mobile number doesn't exist")
    #         if par.is_registered is True:
    #             raise forms.ValidationError("Parent with given mobile number already exists")
    #         return mobile


    def clean_password2(self):
        if 'password' in self.cleaned_data:
            password1 = self.cleaned_data['password']
            password2 = self.cleaned_data['password2']
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            else:
                try:
                    validate_password(password1)
                    return password1
                except exceptions.ValidationError as e:
                    raise forms.ValidationError(e.messages)

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data['password']
        mobile = self.data['mobile']
        email = self.data['email']
        cleaned_data['password'] = make_password(password, make_salt())
        if 'isstudent' in self.data:
            try:
                candidate = Student.objects.get(mobile = mobile)
            except:
                raise forms.ValidationError("Student with given mobile number doesn't exist. Please contact admin!")
            if candidate.email != email:
                raise forms.ValidationError("The entered mobile and email do not match. Please contact admin!")
        else:
            try:
                candidate = Parent.objects.get(mobile=mobile)
            except:
                raise forms.ValidationError("Parent with given mobile number doesn't exist. Please contact admin!")
        if candidate.is_registered is True:
            raise forms.ValidationError("User with given mobile number already exists")
        return cleaned_data


#for email
def make_salt():
    letters = string.ascii_letters
    result = random.sample(letters, 5)
    return ''.join(result)


#for email
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        users = CustomUser.objects.filter(username=self.cleaned_data['username'])
        user = authenticate(username = self.cleaned_data['username'], password=self.cleaned_data['password'])
        if len(users) == 0 and user is None:
            raise forms.ValidationError("Invalid username or password. Please try again!")
        if user is None:
            raise forms.ValidationError("User isn't verified. Please verify using the confirmation link sent to your email")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


#for token
class VerificationForm(forms.Form):
    token_number = forms.CharField(max_length=6, required=True)

    class Meta:
        fields = ('token_number')

    def getToken(self):
        self.full_clean()
