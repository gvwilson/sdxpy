class Person:
    def __init__(self, name):
        self.name = name

class Scientist(Person):
    def __init__(self, name, specialty):
        super().__init__(name)
        self.specialty = specialty

    def __str__(self):
        return f"Scientist(name={self.name}, specialty={self.specialty})"

class Employee(Person):
    def __init__(self, name, department):
        super().__init__(name)
        self.department = department

    def __str__(self):
        return f"Employee(name={self.name}, department={self.department})"

for p in [Scientist("Marie", "biology"), Employee("Ahmed", "R&D")]:
    print(p)
