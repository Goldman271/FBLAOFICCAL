from flet import *
def views_Handler(page):
    def main(page: Page):
        def routeChange(route):
            print(page.route)
        page.views.clear()
        page.views.append(
            views_Handler(page)[page.route]
            
        )
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
    return {
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
            icon=icons.LOGIN,

        ),
        #We're calling the dropdown function here.
                
        (pb),
        
        ]        
        ),
        Column([
            FilledButton(text="Filled button"),
            FilledButton(text="Filled button"),
            FilledButton(text="Filled button"),
        ])
        ),
    ),
    
'Alliance Academy':View(
            route='Alliance Academy',
            controls=[
            AppBar(
            bgcolor="lightBlue",
            title=Text("Welcome to Alliance!", color="White", weight="bold"),
        
        actions=[
        IconButton(
            icon=icons.SEARCH,
            
         ),
        IconButton(
            icon=icons.LOGIN,

        ),
        ]        
        ),


        
            ]
        ),
'Central Forsyth':View(
            route='Central Forsyth',
            controls=[
            AppBar(
            bgcolor="lightBlue",
            title=Text("Welcome to Central Forsyth!", color="White", weight="bold"),
        
        actions=[
        IconButton(
            icon=icons.SEARCH,
            
         ),
        
        IconButton(
            icon=icons.LOGIN,
        ),
        
            ], 
            ),
            ],
      ),   
        
'West Forsyth':View(
            route='West Forsyth',
            controls=[
            AppBar(
            bgcolor="lightBlue",
            title=Text("Welcome to West Forsyth!", color="White", weight="bold"),
        
        actions=[
        IconButton(
            icon=icons.SEARCH,
            
         ),
        IconButton(
            icon=icons.LOGIN,

        ),
        ] 
            )


        
                ]
        )  
    }

    
    

