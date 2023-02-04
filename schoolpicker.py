from flet import *
import sqlite3
'''route to studentHome, parentHome, teacherHome depending on value of typeOfUser'''

con = sqlite3.connect("fblaproject.db",check_same_thread=False)
cur = con.cursor() 
currentValues = []
typeOfUser = cur.execute("""SELECT userType from Users""")
def search(query):
    req = cur.execute("SELECT * FROM School")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == query:
            for i in row:
                currentValues.append(i)
                print(currentValues)
                cur.execute("""
        INSERT INTO Current VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
                con.commit()
        elif str(row[2]) == str(query):
            for i in row:
                currentValues.append(i)
                print(currentValues)
            cur.execute("""
        INSERT INTO Current VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            con.commit()
        else: 
            searchField.error_text = "Hmm, we couldn't find what you were looking for."
            page.update()
searchField = TextField(hint_text="Enter school code or school name...", capitalization="words")
submit = ElevatedButton(text="Search", on_click=lambda _: search(searchField.value))
'''page.add(
    searchField, submit
)'''

class pickSchool(UserControl):
    def build(self):
        searchField = TextField(hint_text="Enter school code or school name...", capitalization="words")
        submit = ElevatedButton(text="Search", on_click=lambda _: search(searchField.value))
        return Row(searchField, submit)