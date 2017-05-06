import hashlib
import random
import smtplib
import base64
# import threading
import threading

from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth import authenticate, login, logout
from django.core.mail.message import EmailMessage
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
from django.template.defaulttags import register
from django.urls.base import reverse, reverse_lazy

from InfoSystem.forms import UserRegistrationForm, UserLoginForm, VerificationForm, UserRegistrationForm2
from InfoSystem.models import CustomUser, Student, Parent, SaltForActivation


@register.filter
def get_item(dict, key):
    return dict.get(key)


@register.filter
def get_list(li, index):
    return li[index]


@register.filter
def get_length(items):
    return len(items)

@register.filter
def get_batch(stud):
    hall = int(stud.hall_ticket[:2])
    if hall < 15:
        return 0
    return 1


def register2(request):
    if request.method == 'POST':
        form = UserRegistrationForm2(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            mobile = form.cleaned_data.get('mobile')
            email = form.cleaned_data.get('email')
            another_mobile = '+91' + mobile
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


#email view
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('email-result-view'))

    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            username = request.POST['username']
            password = request.POST['password']
            if 'isstudent' in form.data:
                user.is_student = True
            else:
                user.is_student = False
            user.save()
            user = authenticate(username=username, password=password)
            user.is_active = False
            user.save()
            id = user.id
            email = user.email
            thread = threading.Thread(target=send_email, args=(email, id, user))
            thread.setDaemon(True)
            thread.start()
            # send_email(email, id, user)
            return render(request, 'thankyou.html')
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('registration/register2.html', context)


#for email view
def activate(request):
    act_key = request.GET.get('id')
    act_key = base64.b64decode(act_key)
    # user = CustomUser.objects.get(id=id)
    user = None
    active_keys = SaltForActivation.objects.all()
    for key in active_keys:
        # salt = key.salt
        email = key.user.email
        id = str(key.user.id)
        # email = "p.priteesh@gmail.com"
        # email = base64.b64encode(str(email))
        temp = email + id
        if temp == act_key:
            user = key.user
            key.delete()
            break
    if user:
        user.is_active = True
        user.save()
        if user.is_student:
            stud = Student.objects.get(mobile=user.mobile)
            stud.user = user
            stud.is_registered = True
            stud.save()
        else:
            stud = Parent.objects.get(mobile=user.mobile)
            stud.user = user
            stud.email = user.email
            stud.is_registered = True
            stud.save()
        return render(request, 'activation.html')


#for email view
def login2(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('email-result-view'))
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.login(request)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('email-result-view'))
                else:
                    return HttpResponse("The user is not verified. Please use the verification sent to email to complete registration")
            return HttpResponseRedirect(reverse('email-result-view'))
    context = {}
    context['next'] = request.GET.get('next')
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('registration/login2.html', context)


#for email view
def send_email(toaddr, id, user):
    # toaddr=u"p.priteesh@gmail.com"
    # salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    email = toaddr
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    salt_for_activation = SaltForActivation(user=user)
    salt_for_activation.save()
    # activation_key = hashlib.sha1(salt+email).hexdigest()
    activation_key = base64.b64encode(email + str(id))
    text = """Hi %s!\nHow are you?\nHere is the link to activate your account: \
           \nhttp://127.0.0.1:8000/activation/?id=%s""" % (user.username, activation_key)
    msg = EmailMessage('CVR Results Site Activation Link', text, to=[toaddr])
    msg.send()


# @login_required(login_url=reverse_lazy('login'))
def otp_verify(request, id):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token_number']
            if token:
                user = CustomUser.objects.get(username=id)
                device = user.twiliosmsdevice_set.get()
                # devices = django_otp.devices_for_user(user)
                if device:
                    status = device.verify_token(token)
                    print status
                    if status:
                        user.is_verified = True
                        user.save()
                        return HttpResponseRedirect(reverse('login'))
                    else:
                        return HttpResponse('User: ' + id + 'could not be verified.' +
                                            '<p><a href="/token/' + id + '/">Click here to generate new token</a></P>')
                else:
                    return HttpResponse('User: ' + id + ' Wrong token!' +
                                        '<p><a href="/token/' + id + '/">Click here to generate new token</a></P>')
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


#for otp view
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
            # return HttpResponseRedirect(reverse('login'))
            if user.is_verified == False:
                return HttpResponse('User: ' + user.username + 'could not be verified.' +
                                    '<p><a href="/token/' + user.username + '/">Click here to generate new token</a></P>')
            return HttpResponseRedirect(reverse('result-view'))

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
    return redirect(reverse('email-login'))


#for otp view
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
            list_of_sem[student] = sem_dict
            print list_of_sem
            sub_achievements = student.ach_subject.all()
            sub_dict = {}
            for ach in sub_achievements:
                index = 'sem' + str((ach.year_of_pursue - 1) * 2 + ach.semester)
                sub_dict.setdefault(index, []).append(ach)
            list_of_subs[student] = sub_dict
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
                            "<p><a href='/token/" + user.username + "/'>Click here to generate new token</a></p>")


# for email view
def result_view2(request):
    user = request.user
    students = []
    if user.is_student is True:
        students.append(Student.objects.get(user=user))
        hall_ticket = int(students[0].hall_ticket[:2])
        exam_info = students[0].examinfo.all().order_by('year_of_pursue', 'semester')
        stud_res_dict = {}
        for ei in exam_info:
            index = 'sem' + str((ei.year_of_pursue - 1) * 2 + ei.semester)
            print index
            stud_res_dict.setdefault(index, []).append(ei)
        # num_buttons = len(examinfo)
        if hall_ticket > 15:
            batch = 1
            return render(request, 'results_final_student.html',
                          {'students': students, 'stud_res_dict': sorted(stud_res_dict.iteritems()), 'batch ':batch })
        batch = 0
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
                       'sem_dict': sem_dict, 'sub_dict': sub_dict, 'batch': batch})

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
        hall = int(student.hall_ticket[:2])
        if hall < 15:
            sem_achievements = student.achievementinasemester.all()
            for ach in sem_achievements:
                index = 'sem' + str((ach.examinfo.year_of_pursue - 1) * 2 + ach.examinfo.semester)
                sem_dict.setdefault(index, []).append(ach)
            list_of_sem[student] = sem_dict
            print list_of_sem
            sub_achievements = student.ach_subject.all()
            sub_dict = {}
            for ach in sub_achievements:
                index = 'sem' + str((ach.year_of_pursue - 1) * 2 + ach.semester)
                sub_dict.setdefault(index, []).append(ach)
            list_of_subs[student] = sub_dict
            print list_of_subs
    for stud, ei in zip(students, list_of_dicts):
        my_dict[stud] = ei
    print my_dict
    return render(request, 'results_final_parent.html',
                  {'parent': par, 'students': students, 'my_dict': my_dict,
                   'list_of_sem': list_of_sem, 'list_of_subs': list_of_subs
                   })
