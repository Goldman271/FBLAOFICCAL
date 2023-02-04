from flet import *
import sqlite3
from flet.security import encrypt, decrypt
from cryptography.fernet import Fernet
import os
secret = os.getenv("MY_APP_SECRET_KEY")
#key = Fernet.generate_key()
#fernet = Fernet(key)
#def main(page:Page):
def authenticate(user, key):
    con = sqlite3.connect("fblaproject.db", check_same_thread=False)
    cur = con.cursor()
    userList = (cur.execute("SELECT * FROM Users")).fetchall()
    print(userList)
    match=False
    for i in userList:
        if user == i[0] or user == i[1]:
            match = True
            if key == i[2]:
                if i[3] == "Student":
                    return "/studentHome"
                elif i[3] == "Parent":
                    return "/parentHome"
                elif i[3] == "Teacher":
                    return "/educatorHome"
            else:
                password.error_text = "Incorrect password."
                page.update()
        else:
            continue
    if match==False:
        username.error_text = "Account not found"
    page.update()
def createAcct():
    page.clean()
    usertype = Dropdown(autofocus = True, options=
                        [dropdown.Option("Student"), dropdown.Option("Parent"), dropdown.Option("Teacher")],)
    newUser = TextField(label = "Type your new username")
    newUserEmail = TextField(label = "Type your email", keyboard_type="email")
    pwd = TextField(label = "Set a password", password=True, can_reveal_password=True)
    verifypwd = TextField(label = "Verify password", password=True, can_reveal_password=True)
    def init():
        if pwd.value == verifypwd.value:
            print(type(pwd.value))
            con = sqlite3.connect("fblaproject.db", check_same_thread=False)
            cur = con.cursor()
            cur.execute("""INSERT INTO Users VALUES(?, ?, ?, ?, ?)""", (newUser.value, newUserEmail.value, pwd.value, "", usertype.value))
            con.commit()
            if usertype.value == "Student":
                return "/studentHome"
            elif usertype.value == "Parent":
                return "/parentHome"
            elif usertype.value == "Teacher":
                return "/educatorHome"
        else:
            verifypwd.error_text = "Hmm, those passwords don't match."
            page.update()
    submit = ElevatedButton(text="Submit", on_click = lambda _: init())
    page.add(newUser, newUserEmail, pwd, verifypwd, usertype, submit)

username = TextField(label = "Type username or email")
password = TextField(label = "Password", password=True, can_reveal_password= True)
submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username.value, password.value)) 
createAccount = TextButton(text = "Don't have an account?", on_click = lambda _: createAcct())
#page.add(username, password, submit, createAccount)

#app(target=main)
class loginField(UserControl):
    def build(self):
        username = TextField(label = "Type username or email")
        password = TextField(label = "Password", password=True, can_reveal_password= True)
        submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username, password)) 
        createAccount = TextButton(text = "Don't have an account?", on_click = lambda _: createAcct())
        return Column(username, password, submit, createAccount)


