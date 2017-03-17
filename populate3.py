from InfoSystem.models import *
import xlrd
import sys
import os
import django

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject1.settings")
book = xlrd.open_workbook("results2.xls")

sheet = book.sheet_by_name("Sheet8")


for row in range(sheet.nrows):
    sub_code = str(sheet.cell(row, 2).value).strip()
    sub_name = str(sheet.cell(row, 3).value).strip()
    sub = Subject.objects.filter(subject_code=sub_code)
    if sub.count() == 0:
        sub = Subject(subject_code=sub_code, name=sub_name)
        sub.save()

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
            exam_object = ExamInfo(year_of_calendar=2016, month_of_year='April', year_of_pursue_roman='III',
                                       semester_roman='II', year_of_pursue=3, semester=2, supple=True, student=stud)
            exam_object.save()
            i=1

        # hall2 = hall1

        sub_code = str(sheet.cell(row, 2).value).strip()
        sub = Subject.objects.get(subject_code=sub_code)
        # Modify the below code accordingly
        exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=3, semester=2, supple=True)
        result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                        credits=credits, examinfo=exam_object)
        result.save()
    except:
        print sys.exc_info()