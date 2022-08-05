class Adder:
    def __init__(self, value):
        self.value = value

    def __call__(self, arg):
        return arg + self.value


add_3 = Adder(3)
result = add_3(8)
print(f"add_3(8): {result}")
