def make_hidden(thing):
    def _inner():
        return thing
    return _inner

has_secret = make_hidden(1 + 2)
print("hidden thing is", has_secret())
