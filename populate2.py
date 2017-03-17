import xlrd
from InfoSystem.models import Parent, Student, Subject, Result, ExamInfo, Branch
from MajorProject1 import settings
import sys
import os
import django

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject1.settings")
book = xlrd.open_workbook("results2.xls")

sheet = book.sheet_by_name("Sheet1")
for row in range(sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count() == 0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
hall2 = ""
i = 0
for row in range(sheet.nrows):
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
        # hall1 = hall_ticket

        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)

        # if hall1 != hall2:  # Populating the ExamInfo table
        if i == 0:
            exam_object = ExamInfo(year_of_calendar=2013, month_of_year=months[11], year_of_pursue_roman='I',
                                       semester_roman='I', year_of_pursue=1, semester=1, supple=False, student=stud)
            exam_object.save()
            i=1

        # hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        # Modify the below code accordingly
        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=1, semester=1)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                        credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()

sheet = book.sheet_by_name("Sheet2")
for row in range(sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count() == 0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#               'November', 'December']
# hall2 = ""
i=0
for row in range(sheet.nrows):
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
        # hall1 = hall_ticket

        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)

        # if hall1 != hall2:  # Populating the ExamInfo table
        if i == 0:
            exam_object = ExamInfo(year_of_calendar=2014, month_of_year=months[3], year_of_pursue_roman='I',
                                           semester_roman='II', year_of_pursue=1, semester=2, supple=False, student=stud)
            exam_object.save()
            i=1

        # hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        # Modify the below code accordingly
        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=1, semester=2)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                            credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()

sheet = book.sheet_by_name("Sheet3")
for row in range(sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count() == 0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#               'November', 'December']
# hall2 = ""
i=0
for row in range(sheet.nrows):
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
        # hall1 = hall_ticket

        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)

        # if hall1 != hall2:
        #  Populating the ExamInfo table
        if i == 0:
            exam_object = ExamInfo(year_of_calendar=2014, month_of_year=months[7], year_of_pursue_roman='II',
                                       semester_roman='I', year_of_pursue=2, semester=1, supple=False, student=stud)
            exam_object.save()
            i=1

        # hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        # Modify the below code accordingly
        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=2, semester=1)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                            credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()

sheet = book.sheet_by_name("Sheet4")
for row in range(sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count() == 0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

i = 0
# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#               'November', 'December']
# hall2 = ""
for row in range(sheet.nrows):
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
        # hall1 = hall_ticket

        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)

        # if hall1 != hall2:  # Populating the ExamInfo table
        if i == 0:
            exam_object = ExamInfo(year_of_calendar=2015, month_of_year=months[3], year_of_pursue_roman='II',
                                           semester_roman='II', year_of_pursue=2, semester=2, supple=False, student=stud)
            exam_object.save()
            i=1

        # hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        # Modify the below code accordingly

        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=2, semester=2)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                            credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()

sheet = book.sheet_by_name("Sheet5")
for row in range(sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count() == 0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#               'November', 'December']
i=0
# hall2 = ""
for row in range(sheet.nrows):
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
        # hall1 = hall_ticket

        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)

        # if hall1 != hall2:  # Populating the ExamInfo table
        if i == 0:
            exam_object = ExamInfo(year_of_calendar=2015, month_of_year=months[8], year_of_pursue_roman='III',
                                           semester_roman='I', year_of_pursue=3, semester=1, supple=False, student=stud)
            exam_object.save()
            i=1
        # hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        # Modify the below code accordingly
        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=3, semester=1)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                            credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()

sheet = book.sheet_by_name("Sheet6")
for row in range(sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count() == 0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#               'November', 'December']
# hall2 = ""
i=0
for row in range(sheet.nrows):
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
        # hall1 = hall_ticket

        print hall_ticket, " in results table"
        stud = Student.objects.get(hall_ticket=hall_ticket)

        # if hall1 != hall2:  # Populating the ExamInfo table
        if i == 0:
            exam_object = ExamInfo(year_of_calendar=2016, month_of_year=months[10], year_of_pursue_roman='IV',
                                           semester_roman='I', year_of_pursue=4, semester=1, supple=False, student=stud)
            exam_object.save()
            i=1

        # hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        # Modify the below code accordingly
        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=4, semester=1)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                            credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()



# from _mysql import IntegrityError
#
# import MySQLdb
# import xlrd
# from InfoSystem.models import Parent, Student, Subject, Result
# from MajorProject1 import settings
#
# import os
# import django
#
# django.setup()
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject1.settings")
#
# #populate parent table
# # Open the workbook and define the worksheet
# book = xlrd.open_workbook("info.xls")
#
#
# for i in range(0, 7):
#     sheet = book.sheet_by_index(i)
#     for row in range(5, sheet.nrows):
#         father_name = str(sheet.cell(row, 9).value).strip()
#         try:
#             father_mobile = str(int(sheet.cell(row, 11).value)).strip()
#         except:
#             father_mobile = None
#         print "Father: ", father_name
#         try:
#             par = Parent(name=father_name, mobile=father_mobile)
#             par.save()
#         except:
#             pass
#
# #populate student table
# for i in range(0, 7):
#     sheet = book.sheet_by_index(i)
#     for row in range(5, sheet.nrows):
#         father_name = str(sheet.cell(row, 9).value).strip()
#         try:
#             father_mobile = str(int(sheet.cell(row, 11).value)).strip()
#         except:
#             father_mobile=None
#         hall_ticket = str(sheet.cell(row, 1).value).strip()
#         print hall_ticket
#         name = str(sheet.cell(row, 2).value).strip()
#         # print "student: ", name
#         try:
#             gender = int(sheet.cell(row, 8).value)
#         except:
#             gender = None
#         if gender == 0:
#             gender = 'MALE'
#         elif gender == 1:
#             gender = 'FEMALE'
#         mother_name = str(sheet.cell(row, 10).value).strip()
#         try:
#             student_mobile = str(int(sheet.cell(row, 12).value)).strip()
#         except:
#             student_mobile = 0
#         email = str(sheet.cell(row, 13).value).strip()
#         object = Parent.objects.filter(mobile=father_mobile)[0]
#         stud = Student(name=name, hall_ticket=hall_ticket, gender=gender, mother_name=mother_name,
#                        father_name=father_name, student_mobile=student_mobile, email=email, parent_mobile=father_mobile,
#                        parent=object)
#         stud.save()
#
#
# #populate subject table
# book = xlrd.open_workbook("results.xls")
# sheet = book.sheet_by_name("TSheet")
#
# for row in range(4, sheet.nrows):
#     sub_code = str(sheet.cell(row, 2).value).strip()
#     sub_name = str(sheet.cell(row, 3).value).strip()
#     sub = Subject.objects.filter(subject_code=sub_code)
#     if sub.count()==0:
#         sub = Subject(subject_code=sub_code, name=sub_name)
#         sub.save()
#
#
# #populate result table
# for row in range(4, sheet.nrows):
#     try:
#         int_marks = str(int(sheet.cell(row, 4).value))
#     except:
#         int_marks = str(sheet.cell(row, 4).value)
#     try:
#         ext_marks = str(int(sheet.cell(row, 5).value))
#     except:
#         ext_marks = str(sheet.cell(row, 5).value)
#
#     res = str(sheet.cell(row, 7).value).strip()
#     credits = int(sheet.cell(row, 8).value)
#     try:
#         hall_ticket = str(sheet.cell(row, 0).value).strip()
#         print hall_ticket, " in results table"
#         stud = Student.objects.get(hall_ticket=hall_ticket)
#         sub_code = str(sheet.cell(row, 2).value).strip()
#         sub = Subject.objects.get(subject_code=sub_code)
#
#         result = Result(student=stud, subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
#                         credits=credits)
#         result.save()
#     except:
#         pass
