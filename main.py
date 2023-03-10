from flet import *
import sqlite3
from schoolClass import School
import datetime
import random
def main(page: Page):
    page.scroll = ScrollMode.ADAPTIVE
    page.theme = Theme(color_scheme_seed="#d9cea9", font_family= "Quire Sans")
    page.window_width = 393
    page.window_height = 700
    page.window_resizable = False
    page.update()


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
            nearmatch = 0
            results = ListView()
            if row[0] == query:
                for i in row:
                    currentValues.append(i)
                    print(currentValues)
                page.session.set("schoolInfo", currentValues)
                if typeOfUser == "Student":
                    page.go("/studentHome2")
                elif typeOfUser == "Parent":
                    page.go("/parentHome2")
                elif typeOfUser == "Teacher":
                    page.go("/educatorHome2")
            elif row[0] in query or query in row[0]:
                results.controls.append(row[0])
                if nearmatch == 0:
                    page.add(results)
                    nearmatch+=1
                else: page.update()
            elif str(row[2]) == str(query):
                for i in row:
                    currentValues.append(i)
                    print(currentValues)
                page.session.set("schoolInfo", currentValues)
                if typeOfUser == "Student":
                    page.go("/studentHome2")
                elif typeOfUser == "Parent":
                    page.go("/parentHome2")
                elif typeOfUser == "Teacher":
                    page.go("/educatorHome2")
            else:
                searchField.error_text = "Hmm. We didn't recognize that school"
                page.update()
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
                page.go("/auth")
            elif usertype.value == "Parent":
                page.go("/auth")
            elif usertype.value == "Teacher":
                page.go("/auth")
        else:
            verifypwd.error_text = "Hmm, those passwords don't match."
            page.update()
    
    def enableButton():
        if createBtn.disabled ==True:
            createBtn.disabled = False
        else:
            createBtn.disabled = True
        page.update()
    def show_terms():
        termsAndCnds.open = True
        page.update()
    termsAndCnds = AlertDialog(content = Text("These terms govern the use of this application and any other related agreement or legal relationship with the Owner in a legally binding way. \n This app is provided by InitTogether \n 1100 Lanier 400 Parkway, Cumming, GA, 30040 \n Terms of Use \n Account Registration \n To use the Service Users must register or create a User account, providing all required data or information in a complete and truthful manner. \n Failure to do so will cause unavailability of the Service. \n Users are responsible for keeping their login credentials confidential and safe. For this reason, Users are also required to choose passwords that meet the highest standards of strength permitted by this Application. \n By registering, Users agree to be fully responsible for all activities that occur under their username and password. Users are required to immediately and unambiguously inform the Owner via the contact details indicated in this document, if they think their personal information, including but not limited to User accounts, access credentials or personal data, have been violated, unduly disclosed or stolen. \n Copyright (c) 2023 InitTogether \n \n Permission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the Software), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE."))
    agree = Checkbox(value = False, on_change = lambda _: enableButton(), label = "By checking this box, I acknowledge that I accept the licensing and terms of use.")
    showTerms = TextButton(text = "View terms", on_click = lambda _: show_terms())
    createBtn = ElevatedButton(text="Submit", disabled = True, on_click = lambda _: init())

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
        user = str(page.session.get("CurrentUser")[5])
        page.pubsub.send_all(f"{user}: {message.value}")
        timestamp = datetime.datetime.now()
        cur = con.cursor()
        recipient = selectRecipient.value #is there a way to check who is getting these messages? that's what belongs in the recipient box
        cur.execute("""INSERT INTO Messages VALUES(?, ?, ?, ?)""", (user, message.value, timestamp, recipient))
        con.commit()
        # clean up the form
        message.value = ""
        page.update()

    #message sending
    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()

    getUsersOfType = """SELECT name FROM Users WHERE UserType = (?)"""
    teacherList = cur.execute(getUsersOfType, ("Teacher",))
    options = []
    for i in teacherList:
        opt = dropdown.Option(i[0])
        options.append(opt)
    selectRecipient = Dropdown(options = options)


    page.overlay.append(pick_files_dialog)

    page.add(
        Row(
            [
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
            ]
        )
    )
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
            dlg = AlertDialog(content = Text("Absence has been reported."))
            dlg.open = True
            page.update()
            page.go('/parentHome2')
        else:
            studentField.error_text = "Student name not recognized"
            page.update()
    submitAbsence = ElevatedButton(text = "Report", on_click = lambda _: updateDB())

    #create sticky notes for upcoming events
    class Event():
        def __init__(self, title, date, time, description):
            self.title = title,
            self.date = date,
            self.time = time,
            self.description = description,
            self.school = page.session.get("schoolInfo")[0]

    def createEvent():
        x = Event(title.value, date.value, time.value, description.value)
        cur.execute("""INSERT INTO Event VALUES(?, ?, ?, ?, ?)""", (title.value, date.value, time.value, description.value, x.school))
        con.commit()
        dlg = AlertDialog(content = Text("Event has been created."), on_dismiss=page.go("/educatorHome2"))
        dlg.open = True
        page.update()
        page.go("/educatorHome2")
    title = TextField(label = "Name of event")
    date = TextField(label = "Date of event", keyboard_type="datetime")
    time = TextField(label = "Time of event", keyboard_type="datetime")
    description = TextField(label = "Description")
    createEventBtn = ElevatedButton(text = "Create Event", on_click = lambda _: createEvent())

    #navigation redirect
    def reroute():
        typeOfUser = page.session.get("CurrentUser")[4]
        if typeOfUser == "Student":
            page.go("/studentHome2")
        elif typeOfUser == "Parent":
            page.go("/parentHome2")
        elif typeOfUser == "Teacher":
            page.go("/educatorHome2")
    #actual page
    page.title = "InitTogether"
    def route_change(route):
        print(page.route)
        page.views.clear()
        if page.route == "/":
            page.views.append(View("/", [Stack([Image(src = f"/together.png"), IconButton(icon = icons.START, on_click = lambda _: page.go("/auth"))])]))
        elif page.route == "/auth":
            page.views.append(
                View(
                "/auth",
                [AppBar(title = Text("InitTogether"), bgcolor=colors.SURFACE_VARIANT), username, password, submit, goToCreate]
                ),)
        elif page.route == "/createAccount":
            page.views.append(
                View(
                "/createAccount",
                [AppBar(title = Text("Create Account"), bgcolor=colors.SURFACE_VARIANT), name, usertype, newUser, newUserEmail, pwd, verifypwd, termsAndCnds, agree, showTerms, createBtn]
                )
            )
        elif page.route == "/schoolSelect":
            list = cur.execute("SELECT name FROM School")
            for i in list:
                y = TextButton(text = "Select")
            page.views.append(View(
            "/schoolSelect",
            [AppBar(title = Text("Search"), bgcolor = colors.SURFACE_VARIANT), searchField, searchBtn]
            ),) 
        elif page.route == "/createSchool":
            page.views.append(View(
                "/createSchool",
                [AppBar(title = Text("Create School"), bgcolor = colors.SURFACE_VARIANT, actions = [
                    IconButton(
                        icon = icons.ARROW_BACK,
                        icon_color = colors.BLACK,
                        tooltip = "Back",
                        on_click = lambda _: page.go("/educatorHome2")
                    )
                ]), nameField, countyField, createSchoolBtn]
            ),)
        elif page.route == "/studentHome":
            page.views.append(View(
            "/studentHome",
            [AppBar(title = Text("Choose School"), bgcolor = colors.SURFACE_VARIANT, actions = [
                    IconButton(
                        icon = icons.LOGOUT,
                        icon_color=colors.BLACK,
                        tooltip = "Logout",
                        on_click=lambda _: page.go("/auth")
                    )
            ]), 
            ElevatedButton(text = "Select school", on_click = lambda _: page.go('/schoolSelect'))],
            ),)
        elif page.route == "/studentHome2":
            grid = GridView(runs_count=3, child_aspect_ratio=0.5)
            page.add(grid)
            colorsList = [colors.YELLOW_50, colors.PURPLE_200, colors.LIGHT_BLUE_100, colors.GREEN_100, colors.PINK_100, colors.SURFACE_VARIANT, colors.BLUE_GREY_100, colors.CYAN_100, colors.ORANGE_100]
            school = page.session.get("schoolInfo")[0]
            EventsList = cur.execute("""SELECT * from Event""").fetchall()
            for i in EventsList:
                if str(i[4]) == str(school):
                    print(i)
                    container = Container(bgcolor = random.choice(colorsList), content = Text(f"{i[0]} \n {i[1]} @ {i[2]} \n {i[3]}", style = TextThemeStyle.TITLE_MEDIUM))
                    grid.controls.append(container)
                else: continue
            if grid.controls == []:
                msg = Text("No upcoming events.")
                page.add(msg)
            
            page.views.append(View(
                "/studentHome2",
                [AppBar(title = Text(page.session.get("schoolInfo")[0]), bgcolor = colors.SURFACE_VARIANT, actions = [
                    IconButton(
                        icon = icons.SHOPPING_CART,
                        icon_color = colors.BLACK,
                        tooltip = "School Store",
                        on_click = lambda _: page.go("/schoolStore")
                    ),
                    IconButton(
                        icon = icons.LOGOUT,
                        icon_color=colors.BLACK,
                        tooltip = "Logout",
                        on_click=lambda _: page.go("/auth")
                    ),
                    IconButton(
                        icon = icons.MESSAGE_OUTLINED,
                        icon_color = colors.BLACK,
                        tooltip = "Messages",
                        on_click = lambda _: page.go('/messages')
                    )
                ],), grid, IconButton(icon = icons.CALENDAR_MONTH, on_click = lambda _: page.go("/calendar"))]
            ))
        elif page.route == "/parentHome":
            page.views.append(View(
            "/parentHome",
            [AppBar(title = Text("Logged in as parent"), bgcolor=colors.SURFACE_VARIANT, actions = [
                    IconButton(
                        icon = icons.LOGOUT,
                        icon_color=colors.BLACK,
                        tooltip = "Logout",
                        on_click=lambda _: page.go("/auth")
                    )
            ]), ElevatedButton(text = "Select school", on_click = lambda _: page.go('/schoolSelect'))]
            ),)
        elif page.route == "/parentHome2":
            grid = GridView(runs_count=3)
            page.add(grid)
            colorsList = [colors.YELLOW_50, colors.PURPLE_200, colors.LIGHT_BLUE_100, colors.PINK_100, colors.SURFACE_VARIANT, colors.BLUE_GREY_100, colors.CYAN_100, colors.ORANGE_100]
            school = page.session.get("schoolInfo")[0]
            EventsList = cur.execute("""SELECT * from Event""").fetchall()
            for i in EventsList:
                if str(i[4]) == str(school):
                    print(i)
                    #controls = Column(Text(f"{i[0]}", style = TextThemeStyle.TITLE_MEDIUM), Text(f"{i[1]}", style = TextThemeStyle.TITLE_MEDIUM), Text(f"{i[2]}", style = TextThemeStyle.TITLE_MEDIUM))
                    container = Container(bgcolor = random.choice(colorsList), content = Text(f"{i[0]} \n {i[1]} @ {i[2]} \n {i[3]}", style = TextThemeStyle.TITLE_MEDIUM))
                    grid.controls.append(container)
                else: continue
            if grid.controls == []:
                msg = Text("No upcoming events.")
                page.add(msg)
            page.views.append(View(
                "/parentHome2",
                [
                AppBar(title = Text(page.session.get("schoolInfo")[0]), bgcolor = colors.SURFACE_VARIANT, actions = [
                    IconButton(
                        icon = icons.SHOPPING_CART,
                        icon_color = colors.BLACK,
                        tooltip = "School Store",
                        on_click = lambda _: page.go("/schoolStore")
                    ),
                    IconButton(
                        icon = icons.MESSAGE_OUTLINED,
                        icon_color = colors.BLACK,
                        tooltip = "Messages",
                        on_click = lambda _: page.go('/messages')
                    ),
                    IconButton(
                        icon = icons.LOGOUT,
                        icon_color=colors.BLACK,
                        tooltip = "Logout",
                        on_click=lambda _: page.go("/auth")
                    ),
            ]), ElevatedButton(text = "Report Absence", on_click = lambda _: page.go('/reportAbsence')), grid, IconButton(icon = icons.CALENDAR_MONTH, on_click = lambda _: page.go("/calendar"))]
            ))
        elif page.route == '/reportAbsence':
            page.views.append(View(
                "/reportAbsence",
                [AppBar(title = Text("Create Event"), actions = [IconButton(
                        icon = icons.ARROW_BACK,
                        icon_color = colors.BLACK,
                        tooltip = "Exit",
                        on_click = lambda _: reroute())]),studentField, reason, submitAbsence]
            ))
        elif page.route == "/educatorHome":
            page.views.append(View(
            "/educatorHome",
            [ElevatedButton(text = "Select school", on_click = lambda _: page.go('/schoolSelect')), TextButton(text = "Create new school", on_click = lambda _: page.go("/createSchool"))]
            ),
        )
        elif page.route == '/educatorHome2':
            grid = GridView(runs_count=3, child_aspect_ratio=0.5, width = page.width)
            page.add(grid)
            colorsList = [colors.YELLOW_50, colors.PURPLE_200, colors.LIGHT_BLUE_100, colors.GREEN_100, colors.PINK_100, colors.SURFACE_VARIANT, colors.BLUE_GREY_100, colors.CYAN_100, colors.ORANGE_100]
            school = page.session.get("schoolInfo")[0]
            EventsList = cur.execute("""SELECT * from Event""").fetchall()
            for i in EventsList:
                if str(i[4]) == str(school):
                    print(i)
                    #controls = Column(Text(f"{i[0]}", style = TextThemeStyle.TITLE_MEDIUM), Text(f"{i[1]}", style = TextThemeStyle.TITLE_MEDIUM), Text(f"{i[2]}", style = TextThemeStyle.TITLE_MEDIUM))
                    container = Container(bgcolor = random.choice(colorsList), content = Text(f"{i[0]} \n {i[1]} @ {i[2]} \n {i[3]}", style = TextThemeStyle.TITLE_MEDIUM))
                    grid.controls.append(container)
                else: continue
            if grid.controls == []:
                msg = Text("No upcoming events.")
                page.add(msg)

            createEventBtn2 = ElevatedButton(text = "Create a New Event", on_click = lambda _: page.go("/createEvent"))
            getSchoolStore = """SELECT * FROM SchoolStoreItems WHERE school = (?)"""
            items = cur.execute(getSchoolStore, (page.session.get("schoolInfo")[0],))
            itemsDisplay = GridView(runs_count = 2, expand=1)
            cargos = Column(controls = [Image(src = f"/sp-pgm-dc-11.jpg", height = 100, fit = ImageFit.CONTAIN), Text("Pants"), Text("$40")])
            hoodie2 = Column(controls = [Image(src = f"/365-Organic-Cotton-Hoodie-Chesnut-Brown-1.png", height = 100, fit = ImageFit.CONTAIN), Text("Hoodie #2"), Text("$55")])
            hoodie = Column(controls = [Image(src = f"/hoodie.jpg", height = 100, fit = ImageFit.CONTAIN), Text("Hoodie"), Text("$45")])
            itemsDisplay.controls.append(cargos, hoodie2, hoodie)
            '''for i in items:
                print(i)
                x = Column(controls = [Image(src = i[0], height = 100, fit = ImageFit.CONTAIN), Text(i[1]), Text(i[2])])
                itemsDisplay.controls.append(x)'''

            goToCreateItem = ElevatedButton(text = "Create a New Item", on_click = lambda _: page.go("/createItem"))
            def createItem(a, b, c, d, e):
                cur.execute("INSERT INTO SchoolStoreItems VALUES(?,?,?,?,?)", (a, b, c, d, e))
                con.commit()
                page.go("/educatorHome2")
            itemsColumn = Column(controls = [goToCreateItem, itemsDisplay])
            tabs = Tabs(
                selected_index = 1, 
                animation_duration = 275,
                tabs = [
                    Tab(
                        text = "Edit School Store",
                        content = itemsColumn,
                    ),
                    Tab(
                        text = "Edit Upcoming Events",
                        content = Column(controls = [grid, createEventBtn2]),
                    ),
                ]
            )
            page.views.append(View(
                '/educatorHome2',
                [AppBar(title = Text("Admin"), bgcolor = colors.SURFACE_VARIANT, actions = [
                    IconButton(
                        icon = icons.SHOPPING_CART,
                        icon_color = colors.BLACK,
                        tooltip = "School Store",
                        on_click = lambda _: page.go("/schoolStore")
                    ),
                    IconButton(
                        icon = icons.MESSAGE_OUTLINED,
                        icon_color = colors.BLACK,
                        tooltip = "Messages",
                        on_click = lambda _: page.go('/messages')
                    ),
                    IconButton(
                        icon = icons.LOGOUT,
                        icon_color=colors.BLACK,
                        tooltip = "Logout",
                        on_click=lambda _: page.go("/auth")
                    ),
                ]), tabs]
            ))
        elif page.route == '/messages':
            page.views.append(View(
                '/messages',
                [AppBar(title = Text("Messages"), bgcolor = colors.SURFACE_VARIANT, actions = [
                    IconButton(
                        icon = icons.LOGOUT,
                        icon_color=colors.BLACK,
                        tooltip = "Logout",
                        on_click=lambda _: page.go("/auth")
                    ),
                    IconButton(
                        icon = icons.ARROW_BACK,
                        icon_color = colors.BLACK,
                        tooltip = "Exit",
                        on_click = lambda _: reroute()
                    )
            ]), Row(controls=[ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ), selected_files]), Row(controls = [displayUser, message, send]), Row(controls = [selectRecipient]), messages]))
            
        elif page.route == "/schoolStore":
            getSchoolStore = """SELECT * FROM SchoolStoreItems WHERE school = (?)"""
            items = cur.execute(getSchoolStore, (page.session.get("schoolInfo")[0],))
            itemsDisplay = GridView(runs_count = 2, expand = 0)
            cargos = Column(controls = [Image(src = f"/sp-pgm-dc-11.jpg", height = 100, fit = ImageFit.CONTAIN), Text("Pants"), Text("$40")])
            hoodie2 = Column(controls = [Image(src = f"/365-Organic-Cotton-Hoodie-Chesnut-Brown-1.png", height = 100, fit = ImageFit.CONTAIN), Text("Hoodie #2"), Text("$55")])
            hoodie = Column(controls = [Image(src = f"/hoodie.jpg", height = 100, fit = ImageFit.CONTAIN), Text("Hoodie"), Text("$45")])
            itemsDisplay.controls.append(cargos)
            itemsDisplay.controls.append(hoodie)
            itemsDisplay.controls.append(hoodie2)
            '''for i in items:
                x = Column(controls = [Image(src = i[0], height = 100, fit = ImageFit.CONTAIN), Text(i[1]), Text(i[2])])
                itemsDisplay.controls.append(x)'''
            page.views.append(View('/schoolStore', [AppBar(title = Text("School Store"), actions = [
                    IconButton(
                        icon = icons.LOGOUT,
                        icon_color=colors.BLACK,
                        tooltip = "Logout",
                        on_click=lambda _: page.go("/auth")
                    ),
                    IconButton(
                        icon = icons.ARROW_BACK,
                        icon_color = colors.BLACK,
                        tooltip = "Exit",
                        on_click = lambda _: reroute()
                    )]), itemsDisplay
            ])),
        elif page.route == "/createItem":
            imageField = TextField(label = "Link to image")
            productnameField = TextField(label = "Name of Product")
            priceField = TextField(label = "Price")
            linkField = TextField(label = "Link for payment")
            def createItem(a, b, c, d, e):
                cur.execute("INSERT INTO SchoolStoreItems VALUES(?,?,?,?,?)", (a, b, c, d, e))
                con.commit()
                page.go("/educatorHome2")
            addNewItem = ElevatedButton(text = "Add Item", on_click=lambda _: createItem(imageField.value, productnameField.value, priceField.value, linkField.value, page.session.get("schoolInfo")[0]))
            page.views.append(View('/createItem', [AppBar(title = "Create Event", actions = [IconButton(
                        icon = icons.ARROW_BACK,
                        icon_color = colors.BLACK,
                        tooltip = "Exit",
                        on_click = lambda _: reroute())]),imageField, productnameField, priceField, linkField, addNewItem]))

        elif page.route == "/createEvent":
            createEventColumn = Column(controls = [title, date, time, description, createEventBtn], scroll = ScrollMode.ADAPTIVE)
            page.views.append(View('/createEvent', [AppBar(title = "Create Event", actions = [IconButton(
                        icon = icons.ARROW_BACK,
                        icon_color = colors.BLACK,
                        tooltip = "Exit",
                        on_click = lambda _: reroute())]), createEventColumn]))

        elif page.route == "/calendar":
            x = Image(src = f"/Screenshot 2023-03-09 223135.png")
            page.views.append(View('/calendar', [AppBar(title = Text("Calendar"), actions = [IconButton(
                        icon = icons.ARROW_BACK,
                        icon_color = colors.BLACK,
                        tooltip = "Exit",
                        on_click = lambda _: reroute()
                    )]), x]))

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    print(page.route)
    page.go('/')

app(target=main, assets_dir = "assets")
    