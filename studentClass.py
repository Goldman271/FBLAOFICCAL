class Student:
    def __init__(self, school, id, password, grade):
        self.school = school
        self.id = id
        self.password = password
        self.grade = grade
        self.teachers = []