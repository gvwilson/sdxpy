def wrap(extra):
    def _inner(f):
        return [f(x) for x in extra]
    return _inner

odds = [1, 3, 5]
first = wrap(odds)
print("1.", first(lambda x: 2 * x))

odds = [7, 9, 11]
print("2.", first(lambda x: 2 * x))

evens = [2, 4, 6]
second = wrap(evens)
print("3.", second(lambda x: 2 * x))

evens.append(8)
print("4.", second(lambda x: 2 * x))
