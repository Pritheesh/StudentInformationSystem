from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from django.urls.base import reverse

from InfoSystem.forms import UserRegistrationForm, UserLoginForm
from InfoSystem.models import CustomUser, Student, Parent


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            is_student = form.cleaned_data['isstudent']
            mobile = form.cleaned_data['mobile']
            user = CustomUser.objects.create(username = username,
                                            email = email,
                                            is_student = is_student,
                                            mobile = mobile
                                             )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            if is_student is True:
                stud = Student.objects.get(mobile=mobile)
                stud.is_registered = True
                stud.user = user
            else:
                par = Parent.objects.get(mobile=mobile)
                par.is_registered = True
                par.email = email
                par.user = user
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})