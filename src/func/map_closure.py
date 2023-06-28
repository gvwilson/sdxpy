data = [5, 10, 15]

# [keep]
def multiply_by(amount):
    def _inner(value):
        return amount * value
    return _inner

print(list(map(multiply_by(2), data)))
print(list(map(multiply_by(3), data)))
# [/keep]
