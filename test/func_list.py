def first():
    print("First")

def second():
    print("Second")

def third():
    print("Third")

everything = [first, second, third]
for func in everything:
    func()
