def wrap(label):
    def _decorate(func):
        def _inner(*args):
            print(f"++ {label}")
            func(*args)
            print(f"-- {label}")
        return _inner
    return _decorate

@wrap("wrapping")
def original(message):
    print(f"original: {message}")

original("example")
