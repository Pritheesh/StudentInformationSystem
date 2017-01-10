import MySQLdb

db = MySQLdb.connect("localhost", "root", "1961", "infotestdb")
cursor = db.cursor()

cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DROP TABLE IF EXISTS InfoSystem_Student")
cursor.execute("DROP TABLE IF EXISTS InfoSystem_Parent")
cursor.execute("DROP TABLE IF EXISTS InfoSystem_Subject")
cursor.execute("DROP TABLE IF EXISTS InfoSystem_Result")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")