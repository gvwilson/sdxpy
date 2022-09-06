# [parent]
class Parent:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name": self.name}
# [/parent]

class Child(Parent):
    def __init__(self, name, check):
        super().__init__(name)
        self.check = check

    def to_dict(self):
        return super().to_dict() | {"check": self.check}
