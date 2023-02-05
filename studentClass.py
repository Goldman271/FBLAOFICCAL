from flet import *
import datetime

class Student:
    def __init__(self, school, id, password, grade):
        self.school = school
        self.id = id
        self.password = password
        self.grade = grade
        self.teachers = []
        self.parents = []



#def main(page: Page):
page.title = "Flet Chat"

# subscribe to broadcast messages
def on_message(msg):
    timestamp = datetime.datetime.now()
    messages.controls.append(Text(msg))
    page.update()

page.pubsub.subscribe(on_message)

def send_click(e):
    page.pubsub.send_all(f"{user.value}: {message.value}")
    # clean up the form
    message.value = ""
    page.update()

messages = Column()
user = Text('Student', color='blue')
message = TextField(hint_text="Your message...", expand=True)  # fill all the space
send = ElevatedButton("Send", on_click=send_click)
page.add(messages, Row(controls=[user, message, send]))





#app(target=main)