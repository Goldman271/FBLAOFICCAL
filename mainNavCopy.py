from flet import *
import sqlite3
from authentication import authenticate, createAcct, loginField
from schoolpicker import search
def main(page: Page):
    username = TextField(label = "Type username or email")
    password = TextField(label = "Password", password=True, can_reveal_password= True)
    submit = ElevatedButton(text="Submit", on_click = lambda _: authenticate(username, password))
    create = TextButton(text = "Don't have an account?", on_click = lambda _: createAcct())
    searchField = TextField(hint_text="Enter school code or school name...", capitalization="words")
    submit = ElevatedButton(text="Search", on_click=lambda _: search(searchField.value))
    page.title = "Login"
    def route_change(route):
        print(page.route)
        page.views.clear()
        if page.route == "/":
            page.views.append(
                View(
                "/",
                [username, password, submit, create]
                ),)
        if page.route == "/schoolSelect":
            page.views.append(View(
            "/schoolSelect",
            [searchField, submit]
            ),)
        elif page.route == "/studentHome":
            page.views.append(View(
            "/studentHome",
            [],
            ),)
        elif route == "/parentHome":
            page.views.append(View(
            "/parentHome",
            []
            ),)
        elif route == "/educatorHome":
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
    