from flet import *
from schoolClass import School
def main(page: Page):
    nameField = TextField(capitalization="words", label = "What is the name of your school?")
    countyField = TextField(capitalization="words", label = "What county is your school located in?")
    def create(x, y):
        if nameField.value == "":
            nameField.error_text = "Type the name of your county"
            page.update()
        elif countyField.value == "":
            countyField.error_text = "Type the name of your school"
            page.update()
        else:
            d = School(x, y)
            page.clean()
            page.add(Text("Your school has been registered!"))
    submit = ElevatedButton(text="Create School", on_click= lambda _: create(nameField.value, countyField.value))
    page.add(nameField, countyField, submit)
    
app(target=main)


