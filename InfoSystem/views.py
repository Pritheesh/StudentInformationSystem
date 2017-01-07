from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView

from InfoSystem.models import Student


class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
