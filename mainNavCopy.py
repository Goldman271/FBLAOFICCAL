from flet import *
import sqlite3
from schoolClass import School
import datetime
def main(page: Page):
    con = sqlite3.connect("fblaproject.db", check_same_thread=False)
    cur=con.cursor()
    #function to verify password
    def authenticate(user, key):
        userList = (cur.execute("SELECT * FROM Users")).fetchall()
        match=False
        for i in userList:
            if user == i[0] or user == i[1]:
                match = True
                print("login success")
                page.session.set("CurrentUser", list(i))
                if key == i[2]:
                    if i[4] == "Student":
                        page.go("/studentHome")
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
    #search for schools
    def search(query):
        currentValues = []
        typeOfUser = page.session.get("CurrentUser")[4]
        '''else: 
            usertype = Dropdown(autofocus = True, options=
        [dropdown.Option("Student"), dropdown.Option("Parent"), dropdown.Option("Teacher")],)
            def defineUserType(value):
                if value.value in ["Student", "Parent", "Teacher"]:
                    typeOfUser = usertype.value
                    page.clean()
                else: 
                    usertype.error_text = "Select an option."
            resubmit = ElevatedButton(text = "Submit", on_click = defineUserType(usertype))
            page.add(usertype, resubmit)'''
        cur=con.cursor()
        req = cur.execute("SELECT * FROM School")
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            if row[0] == query:
                for i in row:
                    currentValues.append(i)
                    print(currentValues)
                page.session.set("schoolInfo", currentValues)
                if typeOfUser == "Student":
                    page.go("/studentHome")
                elif typeOfUser == "Parent":
                    page.go("/parentHome")
                elif typeOfUser == "Teacher":
                    page.go("/educatorHome")
            elif str(row[2]) == str(query):
                for i in row:
                    currentValues.append(i)
                    print(currentValues)
                page.session.set("schoolInfo", currentValues)
                if typeOfUser == "Student":
                    page.go("/studentHome")
                elif typeOfUser == "Parent":
                    page.go("/parentHome")
                elif typeOfUser == "Teacher":
                    page.go("/educatorHome")
    username = TextField(label = "Type username or email")
    password = TextField(label = "Password", password=True, can_reveal_password= True)
    submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username.value, password.value))
    goToCreate = TextButton(text = "Don't have an account?", on_click = lambda _: page.go('/createAccount'))
    
    #for schoolpicker
    searchField = TextField(hint_text="Enter school code or school name...", capitalization="words")
    searchBtn = ElevatedButton(text="Search", on_click=lambda _: search(searchField.value))
    
    #for createAccount
    usertype = Dropdown(autofocus = True, options=
    [dropdown.Option("Student"), dropdown.Option("Parent"), dropdown.Option("Teacher")],)
    newUser = TextField(label = "Type your new username")
    newUserEmail = TextField(label = "Type your email", keyboard_type="email")
    pwd = TextField(label = "Set a password", password=True, can_reveal_password=True)
    verifypwd = TextField(label = "Verify password", password=True, can_reveal_password=True)
    name = TextField(label = "What's your name?",capitalization="words")
    def init():
        if pwd.value == verifypwd.value:
            cur = con.cursor()
            cur.execute("""INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?)""", (newUser.value, newUserEmail.value, pwd.value, "", usertype.value, name.value, False))
            con.commit()
            cur.close()
            if usertype.value == "Student":
                page.go("/")
            elif usertype.value == "Parent":
                page.go("/")
            elif usertype.value == "Teacher":
                page.go("/")
        else:
            verifypwd.error_text = "Hmm, those passwords don't match."
            page.update()
    createBtn = ElevatedButton(text="Submit", on_click = lambda _: init())

    #for createSchool
    nameField = TextField(capitalization="words", label = "What is the name of your school?")
    countyField = TextField(capitalization="words", label = "What county is your school located in?")
    def createSchool(x, y):
        if nameField.value == "":
            nameField.error_text = "Type the name of your county"
            page.update()
        elif countyField.value == "":
            countyField.error_text = "Type the name of your school"
            page.update()
        else:
            d = School(x, y)
            cur = con.cursor()
            cur.execute("""
            INSERT INTO School VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (d.name, d.county, d.number, str(d.events), str(d.students), str(d.teachers), str(d.schoolStoreBool), str(d.schoolStore), str(d.editors)))
            con.commit()
            page.go("/educatorHome")
    createSchoolBtn = ElevatedButton(text="Create School", on_click= lambda _: createSchool(nameField.value, countyField.value))

    #PubSub messages

# subscribe to broadcast messages
    def on_message(msg):
        timestamp = datetime.datetime.now()
        messages.controls.append(Text(msg))
        page.update()
    #i still need to save the sender/who it's sent to but idk where to find that info

    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(f"{user}: {message.value}")
        timestamp = datetime.datetime.now()
        cur = con.cursor()
        recipient = [] #is there a way to check who is getting these messages? that's what belongs in the recipient box
        cur.execute("""INSERT INTO Messages VALUES(?, ?, ?, ?)""", (user, message.value, timestamp, recipient))
        con.commit()
        # clean up the form
        message.value = ""
        page.update()

    messages = Column()
    user = page.session.get("CurrentUser")
    if type(user) == list:
        user = page.session.get("CurrentUser")[5]
    else:
        def setUser():
            if userInput.value == "":
                userInput.error_text = "We didn't get a name. Try again?"
            else:
                user = userInput.value
        userInput = TextField(hint_text = "What's your name?")
        submitUsername = ElevatedButton(text = "Enter", on_click = lambda _: setUser())
        page.add(userInput, submitUsername)
    displayUser = Text(user)
    message = TextField(hint_text="Your message...", expand=True)  # fill all the space
    send = ElevatedButton("Send", on_click=send_click)
    page.add(messages, Row(controls=[displayUser, message, send]))

    #report absences
    studentField = TextField(label = "Student Name:", capitalization="words")
    reason = TextField(label = "Reason for absence", multiline=True)
    def updateDB():
        cur = con.cursor()
        x = cur.execute("SELECT name FROM Users").fetchall()
        y = "UPDATE Users SET Absent = 1 WHERE name = (?)"
        checker = [i[0] for i in x]
        if studentField.value in checker:
            cur.execute(y, (studentField.value,))
            page.go('/parentHome')
        else:
            studentField.error_text = "Student name not recognized"
            page.update()
    submitAbsence = ElevatedButton(text = "Report", on_click = lambda _: updateDB())


    #actual page
    page.title = "Our App"
    def route_change(route):
        print(page.route)
        page.views.clear()
        if page.route == "/":
            page.views.append(
                View(
                "/",
                [username, password, submit, goToCreate]
                ),)
        elif page.route == "/createAccount":
            page.views.append(
                View(
                "/createAccount",
                [name, usertype, newUser, newUserEmail, pwd, verifypwd, createBtn]
                )
            )
        elif page.route == "/schoolSelect":
            page.views.append(View(
            "/schoolSelect",
            [searchField, searchBtn]
            ),)
        elif page.route == "/createSchool":
            page.views.append(View(
                "/createSchool",
                [nameField, countyField, createSchoolBtn]
            ),)
        elif page.route == "/studentHome":
            page.views.append(View(
            "/studentHome",
            [ElevatedButton(text = "Search for school", on_click = lambda _: page.go('/schoolSelect'))],
            ),)
        elif page.route == "/studentHome2":
            page.views.append(View(
                "/studentHome2",
                #calendar and stuff goes here
            ))
        elif page.route == "/parentHome":
            page.views.append(View(
            "/parentHome",
            [ElevatedButton(text = "Report Absence", on_click = lambda _: page.go('/reportAbsence'))]
            ),)
        elif page.route == '/reportAbsence':
            page.views.append(View(
                "/reportAbsence",
                [studentField, reason, submitAbsence]
            ))
        elif page.route == "/educatorHome":
            page.views.append(View(
            "/educatorHome",
            []
            ),
        )
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    print(page.route)
    page.go('/')

app(target=main)
    