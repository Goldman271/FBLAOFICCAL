from studentClass import Student
import sqlite3
class School:
    def __init__(self, name, county):
        con = sqlite3.connect("fblaproject.db",check_same_thread=False)
        cur = con.cursor() 
        ct = 0
        self.name = name
        self.county = county
        self.number = 10575 + ct
        self.events = []
        self.students = []
        self.teachers = []
        self.schoolStoreBool = False
        self.schoolStore = []
        self.editors = []
        ct+=1
        cur.execute("""
            INSERT INTO School VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.name, self.county, self.number, str(self.events), str(self.students), str(self.teachers), str(self.schoolStoreBool), str(self.schoolStore), str(self.editors)))
        con.commit()