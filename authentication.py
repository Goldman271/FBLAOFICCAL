from flet import *
import sqlite3
from logbarRoute import views_Handler
#key = Fernet.generate_key()
#fernet = Fernet(key)
def fake(page:Page):
    #handles routing

#login
    def authenticate(user, key):
        def routeChange(route):
            print(page.route)
            page.views.clear()
            page.views.append(
                views_Handler(page)[page.route]
            )
            page.on_route_change = routeChange
        con = sqlite3.connect("fblaproject.db", check_same_thread=False)
        cur = con.cursor()
        userList = (cur.execute("SELECT * FROM Users")).fetchall()
        print(userList)
        match=False
        for i in userList:
            if user == i[0] or user == i[1]:
                match = True
                print("login success")
                page.session.set("CurrentUser", list(i))
                if key == i[2]:
                    if i[4] == "Student":
                        page.go("West Forsyth")
                    elif i[4] == "Parent":
                        page.go("/parentHome")
                    elif i[4] == "Teacher":
                        page.go("/educatorHome")
                else:
                    password.error_text = "Incorrect password."
                    page.update()
            else:
                continue
        if match==False:
            username.error_text = "Account not found"
        page.update()
    #acct creation
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
                    page.go("/")
                elif usertype.value == "Parent":
                    page.go("/")
                elif usertype.value == "Teacher":
                    page.go("/")
            else:
                verifypwd.error_text = "Hmm, those passwords don't match."
                page.update()
        submit = ElevatedButton(text="Submit", on_click = lambda _: init())
        page.add(newUser, newUserEmail, pwd, verifypwd, usertype, submit)

    #basic elements on main view
    username = TextField(label = "Type username or email")
    password = TextField(label = "Password", password=True, can_reveal_password= True)
    submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username.value, password.value)) 
    createAccount = TextButton(text = "Don't have an account?", on_click = lambda _: createAcct())
    page.add(username, password, submit, createAccount)

'''def view_pop(view):
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)

page.on_route_change = route_change
page.on_view_pop = view_pop
print(page.route)'''

app(target=fake)
class loginField(UserControl):
    def authenticate(user, key):
        con = sqlite3.connect("fblaproject.db", check_same_thread=False)
        cur = con.cursor()
        userList = (cur.execute("SELECT * FROM Users")).fetchall()
        print(userList)
        match=False
        for i in userList:
            if user == i[0] or user == i[1]:
                match = True
                print("login success")
                if key == i[2]:
                    if i[4] == "Student":
                        return "/studentHome"
                    elif i[4] == "Parent":
                        return "/parentHome"
                    elif i[4] == "Teacher":
                        return "/educatorHome"
                else:
                    password.error_text = "Incorrect password."
            else:
                continue
        if match==False:
            username.error_text = "Account not found"

    def createAcct():
        usertype = Dropdown(autofocus = True, options=
        [dropdown.Option("Student"), dropdown.Option("Parent"), dropdown.Option("Teacher")],)
        newUser = TextField(label = "Type your new username")
        newUserEmail = TextField(label = "Type your email", keyboard_type="email")
        pwd = TextField(label = "Set a password", password=True, can_reveal_password=True)
        verifypwd = TextField(label = "Verify password", password=True, can_reveal_password=True)
        def init():
            if pwd.value == verifypwd.value:
                con = sqlite3.connect("fblaproject.db", check_same_thread=False)
                cur = con.cursor()
                cur.execute("""INSERT INTO Users VALUES(?, ?, ?, ?, ?)""", (newUser.value, newUserEmail.value, pwd.value, "", usertype.value))
                con.commit()
                if usertype.value == "Student":
                    return "/"
                elif usertype.value == "Parent":
                    return "/"
                elif usertype.value == "Teacher":
                    return "/"
            else:
                verifypwd.error_text = "Hmm, those passwords don't match."
                page.update()
        return Column(newUser, newUserEmail, pwd, verifypwd, usertype, ElevatedButton(text="Submit", on_click = lambda _: init()))
    def build(self):
        username = TextField(label = "Type username or email")
        password = TextField(label = "Password", password=True, can_reveal_password= True)
        submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username, password))
        create = TextButton(text = "Don't have an account?", on_click = lambda _: createAcct())
        return Column(username, password, submit, create)

    


