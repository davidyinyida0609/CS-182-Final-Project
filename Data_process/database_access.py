from getpass import getpass
import mysql.connector

mydb = mysql.connector.connect(
    host = 'DESKTOP-PATJH5I',
    user="calcourse_data_extraction",
    password="David20030609Yin!",
    database="program_courses"
    )
#request connection with mysql database (need change host if it's not running on local)

mycursor = mydb.cursor()
#convert to cursor object

mycursor.execute("select * from data")
#extract data from tabel whose name is "data"
for i in mycursor:
    print(i)