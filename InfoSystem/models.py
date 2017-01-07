from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=128)
    roll_no = models.CharField(max_length=10, primary_key=True)
    gender = models.CharField(max_length=6)
    mother_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    student_mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=128)
    parent_mobile = models.CharField(max_length=15)