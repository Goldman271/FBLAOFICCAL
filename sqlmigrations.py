import sqlite3
con = sqlite3.connect("fblaproject.db", check_same_thread=False)
cur = con.cursor()
#cur.execute("""ALTER TABLE Users ADD COLUMN UserType""")
#con.commit()
cur.execute("DELETE FROM Users")
con.commit()