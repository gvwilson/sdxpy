class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"name={self.name}"


class Online:
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return f"email={self.email}"


class Scientist(Person, Online):
    def __init__(self, name, specialty, email):
        super().__init__(name)
        super(Person, self).__init__(email)
        self.specialty = specialty

    def __str__(self):
        from_person = super().__str__()
        from_online = super(Person, self).__str__()
        our_own = f"specialty={self.specialty}"
        return f"Scientist({from_person}, {from_online}, {our_own})"


marie = Scientist("Marie", "biology", "marie@nobel.org")
print(marie)
