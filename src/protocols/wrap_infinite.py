def original(value):
    print(f"original: {value}")

def logging(value):
    print("before call")
    original(value)
    print("after call")

original = logging
original("example")
