from flet import *
from logbarRoute import views_Handler
View    
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
                text="Central Forsyth High School",  on_click= lambda _: page.go('Central Forsyth'),
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
'Forsyth':View(
    page.add(
        
        
       
        #We are creating the Appbar and some icons and adding them to the page.
        AppBar(
            bgcolor="lightBlue",
            title=Text("Forsyth County FBLA", color="White", weight="bold"),
        
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
        Container(
            
            FilledButton(text="Welcome! Please log in below"),
            alignment= alignment.center
            
            
            
        )
        ),
    )
    }
    





#AAI PAGE STARTS HERE
def aai(page: Page):
        page.add(
            AppBar(
            bgcolor="lightBlue",
            title=Text("Forsyth County FBLA", color="White", weight="bold"),
        
        actions=[
        IconButton(
            icon=icons.SEARCH,
            
         ),
        IconButton(
            icon=icons.LOGIN,

        ),
        ]        
        ),


        )



# if you want to open it on the browser, use this line of code: app(target=main, view=WEB_BROWSER)
app(target=main)