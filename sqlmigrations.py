import sqlite3
con = sqlite3.connect("fblaproject.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE Users(user, email, pwd, schools, UserType, name, Absent)")
cur.execute("CREATE TABLE School(name, county, id, events, students, teachers, schoolStoreBool, schoolStore, editors)")
cur.execute("CREATE TABLE Messages(Sender, content, timestamp, recipient)")
cur.execute("CREATE TABLE Event(title, date, time, description, school)")
cur.execute("CREATE TABLE SchoolStoreItems(image, name, price, link, school)")
con.commit()
