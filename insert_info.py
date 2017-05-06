from django.db import IntegrityError

import xlrd
from InfoSystem.models import Parent, Student, Subject, Result, ExamInfo, Branch
from MajorProject1 import settings
import sys
import os
import django

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject1.settings")

def insert_info(doc, sheets, start):

    # populating branch table
    try:
        branch = Branch(code='01', name='Civil Engineering')
        branch.save()
        branch = Branch(code='02', name='Electrical and Electronic Engineering')
        branch.save()
        branch = Branch(code='03', name='Mechanical Engineering')
        branch.save()
        branch = Branch(code='04', name='Electronic and Communication Engineering')
        branch.save()
        branch = Branch(code='05', name='Computer Science Engineering')
        branch.save()
        branch = Branch(code='10', name='Electronic and Instrumentation Engineering')
        branch.save()
        branch = Branch(code='12', name='Information Technology')
        branch.save()
    except:
        pass
    book = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT, doc.docfile.name))

    # inserting parent data and 7 indicates the number of sheets separated by branches
    for i in range(0, sheets):
        sheet = book.sheet_by_index(i)
        for row in range(start, sheet.nrows):
            father_name = str(sheet.cell(row, 9).value).strip().title()
            try:
                father_mobile = str(int(sheet.cell(row, 11).value)).strip()
            except:
                father_mobile = None
            # print "Father: ", father_name
            mother_name = str(sheet.cell(row, 10).value).strip().title()
            try:
                par = Parent(father_name=father_name, mobile=father_mobile, mother_name=mother_name)
                par.save()
                print "Inserted details of parent - " + father_name
            except IntegrityError:
                par = Parent.objects.get(mobile=father_mobile)
            except Exception as e:
                print e
                print "-------PROBLEM IN INSERTING PARENT INFO OF " + father_name+"-----------"

    # populate student table
    # for i in range(0, 7):
    #     sheet = book.sheet_by_index(i)
    #     for row in range(5, sheet.nrows):
    #         try:
    #             father_mobile = str(int(sheet.cell(row, 11).value)).strip()
    #         except:
    #             father_mobile = None
            hall_ticket = str(sheet.cell(row, 1).value).strip()
            # print hall_ticket
            name = str(sheet.cell(row, 2).value).strip().title()
            try:
                gender = int(sheet.cell(row, 8).value)
            except:
                gender = None
            if gender == 0:
                gender = 'MALE'
            elif gender == 1:
                gender = 'FEMALE'
            try:
                student_mobile = str(int(sheet.cell(row, 12).value)).strip()
            except:
                student_mobile = 0
            branch = Branch.objects.filter(code__exact=hall_ticket[6:8])[0]
            email = str(sheet.cell(row, 13).value).strip()
            # object = Parent.objects.filter(mobile=father_mobile)[0]
            try:
                stud = Student(name=name, hall_ticket=hall_ticket, gender=gender, mobile=student_mobile, email=email,
                               parent=par, branch=branch)
                stud.save()
            except:
                print "---------THERE WAS PROBLEM INSERTING STUDENT DATA OF "+name+"------------"
            print "student: ", name

    print "------------FINISHED INSERTING INFORMATION------------"
    os.remove(os.path.join(settings.MEDIA_ROOT, doc.docfile.name))