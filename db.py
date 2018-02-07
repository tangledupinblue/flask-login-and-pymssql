
# Python Module db
import pymssql

server = ''
user = ''
password = ''
database= 'tempdb'

conn = pymssql.connect(server, user, password, database)

class ADate:
    def __init__(self,theDate):
        self.theDate = theDate

class Customer:
    def __init__(self, data):
        self.Name = data["Name"]
        self.Email = data["Email"]

class DbRepo:
    def __init__(self, conn):
        self.conn = conn

    def date_get(self):
        cursor = self.conn.cursor(as_dict=True)
        cursor.execute('SELECT GETDATE() AS TheDate;')
        thedate = cursor.fetchone()
        return ADate(thedate)

    def Customer_get(self):
        cursor = self.conn.cursor(as_dict=True)
        cursor.execute("SELECT * FROM (VALUES ('bob', 'bob@bob'), ('fred','fred@fred')) AS Users( Name, Email )") 
        rows = cursor.fetchall()
        return [ Customer(row) for row in rows ]


dbRepo = DbRepo(conn)
