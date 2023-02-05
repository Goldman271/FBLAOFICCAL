from flet import *
import sqlite3
from authentication import authenticate, createAcct, loginField
from schoolpicker import pickSchool
from mainNav2 import views_Handler

def main(page: Page):
    def routeChange(route):
        print(page.route)
        page.views.clear()
        page.views.append(
            views_Handler(page)[page.route]
        )

    page.on_route_change = routeChange
    username = TextField(label = "Type username or email")
    password = TextField(label = "Password", password=True, can_reveal_password= True)
    submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username, password))
    create = TextButton(text = "Don't have an account?", on_click = lambda _: createAcct())
    return{
    '/': View(
    page.add(
        username, password, submit, create
    ),
    route = '/'
    ),
    'studentHome': View(
        page.add(Text("this page has yet to be constructed.")), 
        #route = '/studentHome'
    ),
    'parentHome': View(
        page.add(ElevatedButton(text="Report Absence")),
        #route = '/parentHome'
    ),
    'educatorHome': View(
        page.add(Text("this page edits shit")),
        #route = 'educatorHome'
    )
    }

app(target=main)