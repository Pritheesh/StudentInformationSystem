from _mysql import IntegrityError

import MySQLdb
import xlrd
from InfoSystem.models import Parent, Student, Subject, Result, ExamInfo, Branch
from MajorProject1 import settings
import sys
import os
import django

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject1.settings")
#populating branch table
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

#populate parent table
# Open the workbook and define the worksheet
book = xlrd.open_workbook("info.xls")


for i in range(0, 7):
    sheet = book.sheet_by_index(i)
    for row in range(5, sheet.nrows):
        father_name = str(sheet.cell(row, 9).value).strip().title()
        try:
            father_mobile = str(int(sheet.cell(row, 11).value)).strip()
        except:
            father_mobile = None
        print "Father: ", father_name
        mother_name = str(sheet.cell(row, 10).value).strip().title()
        try:
            par = Parent(father_name=father_name, mobile=father_mobile, mother_name=mother_name)
            par.save()
        except:
            pass

#populate student table
for i in range(0, 7):
    sheet = book.sheet_by_index(i)
    for row in range(5, sheet.nrows):
        try:
            father_mobile = str(int(sheet.cell(row, 11).value)).strip()
        except:
            father_mobile=None
        hall_ticket = str(sheet.cell(row, 1).value).strip()
        print hall_ticket
        name = str(sheet.cell(row, 2).value).strip().title()
        # print "student: ", name
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
        branch = Branch.objects.get(code__exact=hall_ticket[6:8])
        email = str(sheet.cell(row, 13).value).strip()
        object = Parent.objects.filter(mobile=father_mobile)[0]
        stud = Student(name=name, hall_ticket=hall_ticket, gender=gender, mobile=student_mobile, email=email,
                       parent=object, branch=branch)
        stud.save()


#populate subject table
book = xlrd.open_workbook("results.xls")
sheet = book.sheet_by_name("TSheet")

for row in range(4, sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count()==0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()


#populate ExamInfo table
# exam_object = ExamInfo(year_of_calendar=2016, month_of_year=4, year_of_pursue=3, semester=2, supple=False)
# exam_object.save()

#populate result table
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
hall2 = ""
for row in range(4, sheet.nrows):
    try:
        int_marks = str(int(sheet.cell(row, 4).value))
    except:
        int_marks = str(sheet.cell(row, 4).value)
    try:
        ext_marks = str(int(sheet.cell(row, 5).value))
    except:
        ext_marks = str(sheet.cell(row, 5).value)

    res = str(sheet.cell(row, 7).value).strip()
    credits = int(sheet.cell(row, 8).value)
    try:
        hall_ticket = str(sheet.cell(row, 0).value).strip()
        hall1 = hall_ticket

        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)

        if hall1 != hall2: #Populating the ExamInfo table
            exam_object = ExamInfo(year_of_calendar=2016, month_of_year=months[3], year_of_pursue_roman='III',
                                   semester_roman='II', year_of_pursue=3, semester=2, supple=False, student=stud)
            exam_object.save()

        hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        #Modify the below code accordingly
        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=3, semester=2)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                        credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()
