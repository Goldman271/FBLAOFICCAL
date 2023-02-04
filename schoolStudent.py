from flet import *
import sqlite3
con = sqlite3.connect("fblaproject.db", check_same_thread=False)
cur = con.cursor()
class StudentView(UserControl):
    pass
