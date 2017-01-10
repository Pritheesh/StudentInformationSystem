from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=128)
    hall_ticket = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    mother_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    student_mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=128)
    parent_mobile = models.CharField(max_length=15)

    def __unicode__(self):
        return self.roll_no


class Parent(models.Model):
    par_id_from_user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    subject_code = models.CharField(max_length=10)
    name = models.CharField(max_length=128)
    max_internal_marks = models.IntegerField()
    max_external_marks = models.IntegerField()

    def __unicode__(self):
        return self.name


class Result(models.Model):
    hall_ticket = models.ForeignKey(Student)
    subject_code = models.ForeignKey(Subject)
    internal_marks = models.IntegerField()
    external_marks = models.IntegerField()
    results = models.CharField(max_length=5)
    credits = models.IntegerField()