def wrap(func):
    def _inner(*args):
        print("before call")
        func(*args)
        print("after call")
    return _inner

@wrap
def original(message):
    print(f"original: {message}")

original("example")
