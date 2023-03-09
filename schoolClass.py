#from studentClass import Student
import sqlite3
class School:
    ct = 0
    def __init__(self, name, county):
        #con = sqlite3.connect("fblaproject.db",check_same_thread=False)
        #cur = con.cursor() 
        self.name = name
        self.county = county
        self.number = 10575 + ct
        self.events = []
        self.students = []
        self.teachers = []
        self.schoolStoreBool = False
        self.schoolStore = []
        self.editors = []
        self.viewers = []
        ct+=1