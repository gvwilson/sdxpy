def make_hidden(thing):
    def _inner():
        return thing
    return _inner

m = make_hidden("example")
print("hidden thing is", m())
