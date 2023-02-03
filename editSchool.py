from flet import *
from schoolClass import School
from schoolpicker import currentValues
def main(page: Page):
    def update():
        #addSchoolStore
        pass
    header = AppBar(bgcolor="lightblue", title = Text(currentValues[0]))
    addStudents = ElevatedButton()
    addEvents = ElevatedButton()
    addTeachers = ElevatedButton()
    if currentValues[6] == False:
        addSchoolStore = ElevatedButton(on_click = update())
    else:
        editSchoolStore = ElevatedButton()
    addEditors = ElevatedButton()
