from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.context_processors import csrf
from django.views.generic.list import ListView

from django import forms

from InfoSystem.models import Student, Parent


class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'

