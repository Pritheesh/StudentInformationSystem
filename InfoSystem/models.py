from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15)
    is_student = models.BooleanField(verbose_name="Student", default=False)


class Parent(models.Model):
    user = models.OneToOneField(CustomUser, null=True)
    mother_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.CharField(max_length=128, null=True)
    is_registered = models.BooleanField(default=False)

    def __unicode__(self):
        return self.father_name


class Branch(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(CustomUser, null=True)
    parent = models.ForeignKey(Parent)
    branch = models.ForeignKey(Branch)
    name = models.CharField(max_length=128)
    hall_ticket = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=6)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=128, null=True)
    is_registered = models.BooleanField(default=False)

    def __unicode__(self):
        return self.hall_ticket


# class Faculty(models.Model):
#     user = models.OneToOneField(CustomUser, null=True)
#     name = models.CharField(max_length=128)
#     roll_no = models.CharField(max_length=10, unique=True)
#     gender = models.CharField(max_length=6)
#     mobile = models.CharField(max_length=15)
#     email = models.CharField(max_length=128, null=True)
#     branch = models.ForeignKey(Branch)
#     is_registered = models.BooleanField(default=False)


class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=128)
    max_internal_marks = models.IntegerField(null=True)
    max_external_marks = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name


class ExamInfo(models.Model):
    student = models.ForeignKey(Student, related_name='examinfo')
    year_of_pursue_roman = models.CharField(max_length=5)
    semester_roman = models.CharField(max_length=2)
    year_of_pursue = models.IntegerField()
    semester = models.IntegerField()
    year_of_calendar = models.IntegerField()
    month_of_year = models.CharField(max_length=15)
    supple = models.BooleanField()
    total = models.CharField(max_length=3, default='0')

    def __unicode__(self):
        if self.supple == False:
            desc = ' Main'
        else:
            desc = ' Supple'
        return self.year_of_pursue_roman+" "+self.semester_roman+desc

    class Meta:
        ordering = ['year_of_pursue', 'semester']


class Result(models.Model):
    subject = models.ForeignKey(Subject, related_name='subjects')
    examinfo = models.ForeignKey(ExamInfo, related_name='result')
    internal_marks = models.CharField(max_length=3)
    external_marks = models.CharField(max_length=3)
    total = models.CharField(max_length=3)
    results = models.CharField(max_length=5)
    credits = models.IntegerField()

    def __unicode__(self):
        return self.subject.name



class AchievementInASemester(models.Model):
    rank = models.IntegerField()
    student = models.ForeignKey(Student)
    examinfo = models.ForeignKey(ExamInfo)

    def __unicode__(self):
        return self.student.hall_ticket+" "+self.examinfo.year_of_pursue_roman+" "+self.examinfo.semester_roman+" "+str(self.rank)

class AchievementInASubject(models.Model):
    rank = models.IntegerField()
    student = models.ForeignKey(Student)
    result = models.ForeignKey(Result)
    year_of_pursue_roman = models.CharField(max_length=5)
    semester_roman = models.CharField(max_length=2)
    semester = models.IntegerField()
    year_of_pursue = models.IntegerField()

    def __unicode__(self):
        return self.student.hall_ticket+" "+self.result.subject.name+" "+str(self.rank)