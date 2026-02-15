class employee():
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = int(base_salary)
    def total_salary(self):
        return self.base_salary

class Manager(employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent
    def total_salary(self):
        return self.base_salary * (1+int(self.bonus_percent)/100)

class Developer(employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects
    def total_salary(self):
        return self.base_salary +int(self.completed_projects)*500

class Intern(employee):
    def __init__(self, name, base_salary):
        super().__init__(name, base_salary)
    def total_salary(self):
        return super().total_salary()

data = list(map(str, input().split()))

def Output_data(obj):
    salary = obj.total_salary()
    print(f"Name: {data[1]}, Total: {salary:.2f}")

if data[0] == "Manager":
    obj = Manager(data[1], data[2], data[3])
    Output_data(obj)
elif data[0] == "Developer":
    obj = Developer(data[1], data[2], data[3])
    Output_data(obj)
elif data[0] == "Intern":
    obj = Intern(data[1], data[2])
    Output_data(obj)