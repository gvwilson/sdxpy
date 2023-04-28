def make_hidden(value):
    def _inner():
        return value
    return _inner


m = make_hidden("example")
print("hidden value is", m())
