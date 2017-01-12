from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.base import View

from InfoSystem.forms import UserForm
from InfoSystem.models import Parent


def register(request):
    form = UserForm(request.POST or None)
    template_name = 'registration/register.html'

    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        mobile = form.cleaned_data['mobile']
        user.set_password(password)
        par = Parent.objects.get(mobile__exact=mobile)
        if(par.is_registered ==  False):
            user.save()
            par.is_registered == True
            par.user = user
        else:
            return render(request, template_name, {'error_message': 'You are already registered', 'form':form})
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('login')

    return render(request, template_name, {'form': form})

def login_user(request):
    template_name = 'registration/login.html'
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('register')
            else:
                return render(request, template_name, {'error_message': 'Your account has been disabled'})
        else:
            return render(request, template_name, {'error_message': 'Wrong Username/Password. Try again'})

    return render(request, template_name)
