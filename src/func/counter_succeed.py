def make_counter():
    value = [0]
    def _inner():
        value[0] += 1
        return value[0]
    return _inner

c = make_counter()
for i in range(3):
    print(c())
