import sqlite3
con = sqlite3.connect("fblaproject.db", check_same_thread=False)
cur = con.cursor()
#cur.execute("""ALTER TABLE Users ADD COLUMN UserType""")
#con.commit()
#cur.execute("ALTER TABLE School ADD COLUMN viewerType")
#cur.execute("""CREATE TABLE Messages(Sender, content, timestamp)""")
#cur.execute("CREATE TABLE Messages(Sender, content, timstamp, recipient)")
con.commit()
