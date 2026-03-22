def make_counter():
    value = 0
    def _inner():
        value += 1
        return value
    return _inner

c = make_counter()
for i in range(3):
    print(c())
