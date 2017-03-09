from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from django.urls.base import reverse

from InfoSystem.forms import UserRegistrationForm
from InfoSystem.models import CustomUser, Student, Parent


def register(request):
    args = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create(username = form.cleaned_data['username'],
                                            email = form.cleaned_data['email'],
                                            is_student = form.cleaned_data['isstudent'],
                                            mobile = form.cleaned_data['mobile']
                                             )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            if form.cleaned_data['is_student'] is True:
                stud = Student.objects.get(mobile=form.cleaned_data['mobile'])
                stud.is_registered = True
                stud.user = user
            else:
                par = Parent.objects.get(mobile=form.cleaned_data['mobile'])
                par.is_registered = True
                par.email = form.cleaned_data['email']
                par.user = user
            return HttpResponseRedirect(reverse('login'))
    form = UserRegistrationForm()
    args['form'] = form
    args.update(csrf(request))
    return render(request, 'registration/register.html', args)
    # return render_to_response('registration/register.html', {'form': form}, RequestContext(request))

def login(request):
    pass