from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.urls.base import reverse

from InfoSystem.forms import UserRegistrationForm, UserLoginForm
from InfoSystem.models import CustomUser, Student, Parent
from MajorProject1 import settings



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if 'isstudent' in form.data:
                if form.data['isstudent'] == 'on':
                    is_student = True
            else:
                is_student = False
            mobile = form.cleaned_data['mobile']
            user = CustomUser.objects.create(username = username,
                                            email = email,
                                            is_student = is_student,
                                            mobile = mobile
                                             )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # user = authenticate(username=username, password=form.cleaned_data['password1'])
            if is_student is True:
                stud = Student.objects.get(mobile=mobile)
                stud.is_registered = True
                stud.user = user
                stud.save()
            else:
                par = Parent.objects.get(mobile=mobile)
                par.is_registered = True
                par.email = email
                par.user = user
                par.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    redirect_authenticated_user = True
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


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def result_view(request):
    user = request.user
    students = []
    if user.is_student is True:
        students.append(Student.objects.get(user=user))
        exam_info = students[0].examinfo.all().order_by('year_of_pursue', 'semester')
        stud_res_dict = {}
        for ei in exam_info:
            index = 'sem' + str((ei.year_of_pursue - 1) * 2 + ei.semester)
            print index
            stud_res_dict.setdefault(index, []).append(ei)
        # num_buttons = len(examinfo)
        return render(request, 'results_final_student.html',
                      {'students': students, 'stud_res_dict': sorted(stud_res_dict.iteritems())})

    par = Parent.objects.get(user=user)
    students = par.student_set.all()
    list_of_dicts = []
    my_dict = {}
    for student in students:
        ei = student.examinfo.all().order_by('year_of_pursue', 'semester')
        temp = {}
        for e in ei:
            index = 'sem' + str((e.year_of_pursue - 1) * 2 + e.semester)
            print index
            temp.setdefault(index, []).append(e)
        print temp
        temp = OrderedDict(sorted(temp.items(), key=lambda x: x[0]))
        print temp
        list_of_dicts.append(temp)

    for stud, ei in zip(students, list_of_dicts):
        my_dict[stud] = ei
    print my_dict
    return render(request, 'results_final_parent.html',
                  {'parent': par, 'students': students, 'my_dict': my_dict})