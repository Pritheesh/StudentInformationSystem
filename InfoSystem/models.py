from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Parent(models.Model):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.CharField(max_length=128, null=True)
    is_registered = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    parent = models.ForeignKey(Parent)
    name = models.CharField(max_length=128)
    hall_ticket = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=6)
    mother_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    student_mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=128, null=True)
    parent_mobile = models.CharField(max_length=15, null=True)

    def __unicode__(self):
        return self.hall_ticket


class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=128)
    max_internal_marks = models.IntegerField(null=True)
    max_external_marks = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name


class Result(models.Model):
    student = models.ForeignKey(Student)
    subject = models.ForeignKey(Subject)
    internal_marks = models.CharField(max_length=3)
    external_marks = models.CharField(max_length=3)
    results = models.CharField(max_length=5)
    credits = models.IntegerField()

    def __unicode__(self):
        return self.subject.name
