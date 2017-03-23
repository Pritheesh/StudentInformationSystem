from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.template.defaulttags import register
from django.urls.base import reverse, reverse_lazy

from InfoSystem.forms import UserRegistrationForm, UserLoginForm, VerificationForm, UserRegistrationForm2
from InfoSystem.models import CustomUser, Student, Parent
from MajorProject1 import settings


@register.filter
def get_item(dict, key):
    return dict.get(key)

@register.filter
def get_list(li, index):
    return li[index]


def register2(request):
    if request.method == 'POST':
        form = UserRegistrationForm2(request.POST)
        if form.is_valid():
            user = form.save()
            mobile = form.cleaned_data.get('mobile')
            email = form.cleaned_data.get('email')
            another_mobile = '+91'+mobile
            if 'isstudent' in form.data:
                is_student = True
            else:
                is_student = False
            if user.id:
                user.is_student = is_student
                user.twiliosmsdevice_set.create(name='SMS', number=another_mobile)
                device = user.twiliosmsdevice_set.get()
                device.generate_challenge()
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
            return HttpResponseRedirect(reverse('otp-verify', args=[user.username]))

    else:
        form = UserRegistrationForm2()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('registration/register.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if 'isstudent' in form.data:
                # if form.data['isstudent'] == 'on':
                is_student = True
            else:
                is_student = False
            mobile = form.cleaned_data['mobile']
            user = form.save(commit=False)
            # user = CustomUser.objects.create(username = username,
            #                                 email = email,
            #                                 is_student = is_student,
            #                                 mobile = mobile
            #                                  )
            # user.set_password(form.cleaned_data['password1'])
            # user.save()
            if user.id:
                user.twiliosmsdevice_set.create(name='SMS', number=mobile)
                device = user.twiliosmsdevice_set.get()
                device.generate_challenge()
                user = authenticate(username=username, password=form.cleaned_data['password1'])
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

                return HttpResponseRedirect('/otp/verify')
            # return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# @login_required(login_url=reverse_lazy('login'))
def otp_verify(request, id):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        token = form.getToken()
        if token:
            user = CustomUser.objects.get(username=id)
            device = user.twiliosmsdevice_set.get()
            #devices = django_otp.devices_for_user(user)
            if device:
                status = device.verify_token(token)
                print status
                if status:
                    user.is_verified = True
                    user.save()
                    return HttpResponseRedirect(reverse('login'))
                else:
                    return HttpResponse('User: ' + id  + 'could not be verified.' +
                                        '<p><a href="/token/'+id+'/">Click here to generate new token</a></P>')
            else:
                return HttpResponse('User: ' + id + ' Wrong token!' +
                                    '<p><a href="/token/'+id+'/">Click here to generate new token</a></P>')
    else:
        form = VerificationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('verify.html', context)


# @login_required(login_url=reverse_lazy('login'))
def otp_token(request, id):
    user = CustomUser.objects.get(username=id)
    device = user.twiliosmsdevice_set.get()
    device.generate_challenge()
    return HttpResponseRedirect(reverse('otp-verify', args=[id]))


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('result-view'))
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None:
                login(request, user)
                if request.POST.get('next') != 'None':
                    return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserLoginForm()
    context = {}
    context['next'] = request.GET.get('next')
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('registration/login.html', context)
    # return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))



def result_view(request):
    user = request.user
    user = CustomUser.objects.get(username=user.username)
    if user.is_verified == True:
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
            sem_achievements = students[0].achievementinasemester.all()
            sem_dict = {}
            for ach in sem_achievements:
                index = 'sem' + str((ach.examinfo.year_of_pursue - 1) * 2 + ach.examinfo.semester)
                sem_dict.setdefault(index, []).append(ach)
            sub_achievements = students[0].ach_subject.all()
            sub_dict = {}
            for ach in sub_achievements:
                index = 'sem' + str((ach.year_of_pursue - 1) * 2 + ach.semester)
                sub_dict.setdefault(index, []).append(ach)
            return render(request, 'results_final_student.html',
                          {'students': students, 'stud_res_dict': sorted(stud_res_dict.iteritems()),
                           'sem_dict': sem_dict, 'sub_dict': sub_dict})

        par = Parent.objects.get(user=user)
        students = par.student_set.all()
        list_of_dicts = []
        my_dict = {}
        list_of_sem = {}
        list_of_subs = {}
        for student in students:
            ei = student.examinfo.all().order_by('year_of_pursue', 'semester')
            temp = {}
            for e in ei:
                index = 'sem' + str((e.year_of_pursue - 1) * 2 + e.semester)
                print index
                temp.setdefault(index, []).append(e)
            # print temp
            temp = OrderedDict(sorted(temp.items(), key=lambda x: x[0]))
            # print temp
            list_of_dicts.append(temp)

            sem_dict = {}
            sem_achievements = student.achievementinasemester.all()
            for ach in sem_achievements:
                index = 'sem' + str((ach.examinfo.year_of_pursue - 1) * 2 + ach.examinfo.semester)
                sem_dict.setdefault(index, []).append(ach)
            list_of_sem[student]=sem_dict
            print list_of_sem
            sub_achievements = student.ach_subject.all()
            sub_dict = {}
            for ach in sub_achievements:
                index = 'sem' + str((ach.year_of_pursue - 1) * 2 + ach.semester)
                sub_dict.setdefault(index, []).append(ach)
            list_of_subs[student]=sub_dict
            print list_of_subs
        for stud, ei in zip(students, list_of_dicts):
            my_dict[stud] = ei
        print my_dict
        return render(request, 'results_final_parent.html',
                      {'parent': par, 'students': students, 'my_dict': my_dict,
                       'list_of_sem': list_of_sem, 'list_of_subs': list_of_subs
                       })
    else:
        return HttpResponse(user.username + " is not verified." +
                            "<p><a href='/token/"+user.username+"/'>Click here to generate new token</a></p>")


