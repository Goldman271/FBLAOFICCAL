from flet import *
from fl import views_Handler
import sqlite3

def main(page: Page):
    con = sqlite3.connect("fblaproject.db",check_same_thread=False)
    cur = con.cursor() 
    currentValues = []
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
    page.add(
        searchField, submit
    )

app(target = main)