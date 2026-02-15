class person():
    def __init__(self, name):
        self.name = name

class student(person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa
    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")

data = list(map(str, input().split()))
p1 = student(data[0], data[1])
p1.display()