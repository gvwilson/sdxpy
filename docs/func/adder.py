def make_adder(to_add):
    def _inner(value):
        return value + to_add
    return _inner

a = make_adder(100)
print(a(1))
