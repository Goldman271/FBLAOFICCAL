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
    
#Below is the code for the dropdown that is seen in the far right on the Appbar.
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update() 
    colors="don't matter",
    pb = PopupMenuButton(
        items=[
           PopupMenuItem(
                text="Central Forsyth High School",  on_click= lambda _: page.go('/studentHome'),
             ),
           PopupMenuItem(),
           PopupMenuItem(
                text="Alliance Academy for Innovation",  on_click= lambda _: page.go('Alliance Academy')
            ),
           PopupMenuItem(),
           PopupMenuItem(
             text="West Forsyth High School", on_click= lambda _: page.go('West Forsyth')
           ),  # divider
            
        ]
    )
    return{
'school':View(
    
        page.add(
            AppBar(
            bgcolor="lightBlue",
            title=Text("County County FBLA", color="White", weight="bold"),
        
        actions=[
        IconButton(
            icon=icons.SEARCH,
            
         ),
        IconButton(
            icon=icons.LOGIN, on_click= lambda _: SystemExit

        ),
        #We're calling the dropdown function here.
        (pb)        

        
        ]        
        ),
            )
    

        
        
        ),
    
    }
    



app(target=main)