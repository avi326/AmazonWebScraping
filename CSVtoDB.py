# convert the csv file to tables in database
from Database import Database

print("Convert CSV to MySQL Database. ")
db = Database.Database()
db.insert_all_to_mysql()
db.close_connect_db()
print("Done. ")