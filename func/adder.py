def make_adder(to_add):
    def _inner(value):
        return value + to_add
    return _inner

adder_func = make_adder(100)
print(adder_func(1))
