import sys
import threading

import xlrd

from InfoSystem.models import Subject, Student, Result, ExamInfo
from insert_ach_in_sem import insert_sem_ach
from insert_ach_in_sub import insert_sub_ach


def insert_results(doc, examinfo, sheets, start):
    book = xlrd.open_workbook(doc.docfile.name)
    sheet = book.sheet_by_index(0)

    #subject table
    for i in range(sheets):
        for row in range(start, sheet.nrows):
            sub_code = str(sheet.cell(row, 2).value).strip()
            sub_name = str(sheet.cell(row, 3).value).strip()
            sub = Subject.objects.filter(subject_code=sub_code)
            if sub.count()==0:
                sub = Subject(subject_code=sub_code, name=sub_name)
                sub.save()
                print "Inserted "+sub_name

        #results
        hall2 = ""
        for row in range(start, sheet.nrows):
            hall_ticket = str(sheet.cell(row, 0).value).strip()
            try:
                int_marks = str(int(sheet.cell(row, 4).value))
            except:
                int_marks = str(sheet.cell(row, 4).value)
            try:
                ext_marks = str(int(sheet.cell(row, 5).value))
            except:
                ext_marks = str(sheet.cell(row, 5).value)
            total_marks = 0
            try:
                total_marks += int(int_marks)
            except:
                print hall_ticket+" was absent for internal "+str(sheet.cell(row, 2).value)
            try:
                total_marks += int(ext_marks)
            except:
                print hall_ticket+" was absent for external"+str(sheet.cell(row, 3).value)
            res = str(sheet.cell(row, 7).value).strip()
            credits = int(sheet.cell(row, 8).value)
            try:
                hall1 = hall_ticket

                # print hall_ticket, " in results table"
                stud = Student.objects.get(hall_ticket=hall_ticket)

                if hall1 != hall2: #Populating the ExamInfo table
                    exam_object = ExamInfo(year_of_calendar=examinfo.year_of_calendar,
                                           month_of_year=examinfo.month_of_year,
                                           year_of_pursue_roman=examinfo.year_of_pursue_roman,
                                           semester_roman=examinfo.semester_roman,
                                           year_of_pursue=examinfo.year_of_pursue,
                                           semester=examinfo.semester,
                                           supple=examinfo.supple,
                                           student=stud)
                    exam_object.save()

                hall2 = hall1

                sub_code = str(sheet.cell(row, 2).value).strip()
                sub = Subject.objects.get(subject_code=sub_code)
                #Modify the below code accordingly
                if not examinfo.supple:
                    exam_object = ExamInfo.objects.get(student=stud, year_of_pursue=examinfo.year_of_pursue, semester=examinfo.semester,
                                                       supple=False)
                    exam_object.total = str(int(exam_object.total) + total_marks)
                    exam_object.save()
                result = Result(subject=sub, internal_marks=int_marks, external_marks=ext_marks, results=res,
                                credits=credits, examinfo=exam_object, total=str(total_marks))
                result.save()
                print "Inserted results of ", hall_ticket
            except:
                print "------------PROBLEM INSERTING DETAILS OF "+hall_ticket+"--------------"
                print sys.exc_info()
    print "------------FINISHED INSERTING RESULTS------------"
    thread = threading.Thread(target=insert_sem_ach, args=(examinfo.year_of_pursue, examinfo.year_of_calendar,
                                                           examinfo.semester, examinfo.month_of_year))
    thread.setDaemon(True)
    thread.start()

    thread = threading.Thread(target=insert_sub_ach, args=(examinfo.year_of_pursue, examinfo.year_of_calendar,
                                                           examinfo.semester, examinfo.month_of_year))
    thread.setDaemon(True)
    thread.start()

    doc.delete()
