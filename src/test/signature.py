def zero():
    print("zero")

def one(value):
    print("one", value)

for func in [zero, one]:
    func()
