import MySQLdb
import xlrd
from InfoSystem.models import Parent
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
sheet = book.sheet_by_name("IT")


query1 = """insert into InfoSystem_parent (name, mobile) VALUES (%s, %s)"""
query2 = """insert into Infosystem_student (name, hall_ticket, gender, mother_name, father_name, student_mobile,
email, parent_mobile, parent_id_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %d)"""

for row in range(5, sheet.nrows):
    father_name = sheet.cell(row, 9).value
    father_mobile = str(int(sheet.cell(row, 11).value))
    values = (father_name.strip(), father_mobile.strip())
    print values
    cursor.execute(query1, values)

db.commit()

for row in range(5, sheet.nrows):
    father_name = sheet.cell(row, 9).value.strip()
    father_mobile = str(int(sheet.cell(row, 11).value)).strip()
    hall_ticket = sheet.cell(row, 1).value.strip()
    name = sheet.cell(row, 2).value.strip()
    gender = str(int(sheet.cell(row, 8).value)).strip()
    mother_name = sheet.cell(row, 10).value.strip()
    student_mobile = str(int(sheet.cell(row, 12).value)).strip()
    email = sheet.cell(row, 13).value.strip()
    object = Parent.objects.get(name=father_name)
    values2 = (name, hall_ticket, gender, mother_name, father_name, student_mobile, email, father_mobile, int(object.id))
    # print values2

    print query2 % values2
    cursor.execute(query2, values2)

db.commit()
db.close()