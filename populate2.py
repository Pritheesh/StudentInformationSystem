import MySQLdb
import xlrd

#populate parent table
# Open the workbook and define the worksheet
book = xlrd.open_workbook("info.xls")
sheet = book.sheet_by_name("IT")

query2 = """insert into Infosystem_student (name, hall_ticket, gender, mother_name, father_name, student_mobile,
email, parent_mobile, parent_id_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %d)"""

db = MySQLdb.connect("localhost", "root", "1961", "infotestdb")
cursor = db.cursor()

i = 1
for row in range(5, sheet.nrows):
    father_name = str(sheet.cell(row, 9).value).strip()
    father_mobile = str(int(sheet.cell(row, 11).value)).strip()
    hall_ticket = str(sheet.cell(row, 1).value).strip()
    name = str(sheet.cell(row, 2).value).strip()
    gender = str(sheet.cell(row, 8).value).strip()
    mother_name = str(sheet.cell(row, 10).value).strip()
    student_mobile = str(int(sheet.cell(row, 12).value)).strip()
    email = str(sheet.cell(row, 13).value).strip()
    values2 = (name, hall_ticket, gender, mother_name, father_name, student_mobile, email, father_mobile, int(i))
    print values2
    i += 1
    cursor.execute(query2, values2)


db.commit()
db.close()