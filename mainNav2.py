from flet import *
def views_Handler(page):
    def main(page: Page):
        def routeChange(route):
            print(page.route)
        page.views.clear()
        page.views.append(
            views_Handler(page)[page.route]
            
        )
    return{
'/school':View(
    
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
         

        
        ]        
        ),
            )
    

        
        
        ),
    
    }