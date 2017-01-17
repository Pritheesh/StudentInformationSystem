from _mysql import IntegrityError

import MySQLdb
import xlrd
from InfoSystem.models import Parent, Student, Subject, Result
from MajorProject1 import settings

import os
import django

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject1.settings")

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
        email = str(sheet.cell(row, 13).value).strip()
        object = Parent.objects.filter(mobile=father_mobile)[0]
        stud = Student(name=name, hall_ticket=hall_ticket, gender=gender, mobile=student_mobile, email=email,
                       parent=object)
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


#populate result table
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
        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)
        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)

        result = Result(student=stud, subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                        credits=credits)
        result.save()
    except:
        pass
