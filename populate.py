from _mysql import IntegrityError

import MySQLdb
import xlrd
from InfoSystem.models import Parent, Student, Subject, Result
from MajorProject1 import settings

import os
import django

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject1.settings")

db = MySQLdb.connect("localhost", "root", "1961", "infotestdb")
cursor = db.cursor()

#populate parent table
# Open the workbook and define the worksheet
book = xlrd.open_workbook("info.xls")

query1 = """insert into InfoSystem_parent (name, mobile) VALUES (%s, %s)"""


for i in range(0, 6):
    sheet = book.sheet_by_index(i)
    for row in range(5, sheet.nrows):
        try:
            father_name = sheet.cell(row, 9).value
            father_mobile = str(int(sheet.cell(row, 11).value))
            values = (father_name.strip(), father_mobile.strip())
            print values
            cursor.execute(query1, values)
        except:
            pass

db.commit()

for row in range(5, sheet.nrows):
    try:
        father_name = sheet.cell(row, 9).value.strip()
        father_mobile = str(int(sheet.cell(row, 11).value)).strip()
        hall_ticket = sheet.cell(row, 1).value.strip()
        name = sheet.cell(row, 2).value.strip()
        gender = str(int(sheet.cell(row, 8).value)).strip()
        mother_name = sheet.cell(row, 10).value.strip()
        student_mobile = str(int(sheet.cell(row, 12).value)).strip()
        email = str(sheet.cell(row, 13).value).strip()
        object = Parent.objects.filter(mobile=father_mobile)[0]
        stud = Student(name=name, hall_ticket=hall_ticket, gender=gender, mother_name=mother_name, father_name=father_name,
                       student_mobile=student_mobile, email=email, parent_mobile=father_mobile, parent_id=object)
        stud.save()
    except:
        pass

book = xlrd.open_workbook("results.xls")
sheet = book.sheet_by_name("TSheet")

for row in range(4, sheet.nrows):
    sub_code = sheet.cell(row, 2).value.strip()
    sub_name = sheet.cell(row, 3).value.strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count()==0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

for row in range(4, sheet.nrows):
    hall_ticket = sheet.cell(row, 0).value.strip()
    print hall_ticket
    stud = Student.objects.get(hall_ticket=hall_ticket)
    sub_code = sheet.cell(row, 2).value.strip()
    sub = Subject.objects.get(subject_code=sub_code)
    try:
        int_marks = str(int(sheet.cell(row, 4).value))
    except:
        int_marks = str(sheet.cell(row, 4).value)
    try:
        ext_marks = str(int(sheet.cell(row, 5).value))
    except:
        ext_marks = str(sheet.cell(row, 5).value)

    res = sheet.cell(row, 7).value
    credits = int(sheet.cell(row, 8).value)

    result = Result(hall_ticket=stud, subject_code=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                    credits=credits)
    result.save()