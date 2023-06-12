def wrap(label):                  # function returning a decorator
    def _decorate(func):          # the actual decorator
        def _inner(*args):        # the wrapped function
            print(f"++ {label}")  # 'label' is visible because
            func(*args)           # it's captured in the closure
            print(f"-- {label}")  # of '_decorate'
        return _inner
    return _decorate

@wrap("wrapping")                 # call 'wrap' to get a decorator
def original(message):            # decorator applied here
    print(f"original: {message}")

original("example")
