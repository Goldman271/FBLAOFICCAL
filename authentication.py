from flet import *
import sqlite3
from flet.security import encrypt, decrypt
def authenticate(user, key):
    con = sqlite3.connect("fblaproject.db", check_same_thread=False)
    cur = con.cursor()
    userList = (cur.execute("SELECT * FROM Users")).fetchall()
    for i in userList:
        if user == i[0]:
            if key == decrypt(i[2]):
                #redirect to appropriate page
                pass
            else:
                password.error_text = "Incorrect password."
                page.update()
        else:
            continue
    username.error_text = "Account not found"
    page.update()
def createAcct():
    newUser = TextField(label = "Type your new username")
    newUserEmail = TextField(label = "Type your email", keyboard_type="email")
    pwd = TextField(label = "Set a password", password=True, can_reveal_password=True)
    verifypwd = TextField(label = "Verify password", password=True, can_reveal_password=True)
    page.add(newUser, newUserEmail, pwd, verifypwd)
    if pwd == verifypwd:
        con = sqlite3.connect("fblaproject.db", check_same_thread=False)
        cur = con.cursor()
        cur.execute("""INSERT INTO Users VALUES(?, ?, ?)""", (newUser, newUserEmail, encrypt(pwd)))
    else:
        verifypwd.error_text = "Hmm, those passwords don't match."
        page.update()

username = TextField(label = "Type username or email")
password = TextField(label = "Password", password=True, can_reveal_password= True)
submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username, password)) 
createAccount = TextButton(text = "Don't have an account?", on_click = lambda _: createAcct())