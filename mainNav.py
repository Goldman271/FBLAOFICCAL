'''from flet import *
import sqlite3
<<<<<<< Updated upstream
from authentication import authenticate, createAcct, loginField
from schoolpicker import pickSchool
=======
from mainNav2 import views_Handler

>>>>>>> Stashed changes
def main(page: Page):
    page.title = "Login"
    def route_change(route):
        print(page.route)
        page.views.clear()
        if page.route == "/":
            page.views.append(
                View(
                "/",
                [loginField()]
                ),)
        if page.route == "/schoolSelect":
            page.views.append(View(
            "/schoolSelect",
            [pickSchool]
            ),)
        elif page.route == "/studentHome":
            page.views.append(View(
            "/studentHome",
            [],
            ),)
        elif page.route == "/parentHome":
            page.views.append(View(
            "/parentHome",
            []
            ),)
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

app(target=main)
'''