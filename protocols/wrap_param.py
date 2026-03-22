def original(value):
    print(f"original: {value}")

def logging(func, label):
    def _inner(value):
        print(f"++ {label}")
        func(value)
        print(f"-- {label}")
    return _inner

original = logging(original, "call")
original("example")
