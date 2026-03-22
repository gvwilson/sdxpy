def original(value):
    print(f"original: {value}")

def logging(func):
    def _inner(value):
        print("before call")
        func(value)
        print("after call")
    return _inner

original = logging(original)
original("example")
