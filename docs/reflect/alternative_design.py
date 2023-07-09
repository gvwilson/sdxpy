def decorator(func, label):
    def _inner(arg):
        print(f"entering {label}")
        func(arg)
    return _inner

@decorator("message")
def double(x):           # equivalent to
    return 2 * x         # double = decorator(double, "message")
