class Pretend:
    def __init__(self, increment):
        self._increment = increment

    def __call__(self, value):
        return value + self._increment

p = Pretend(3)
result = p(10)
print(result)
