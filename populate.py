import MySQLdb
import xlrd

db = MySQLdb.connect("localhost", "root", "1961", "infotestdb")
cursor = db.cursor()

query = """insert into InfoSystem_student VALUES (hall_ticket, )"""