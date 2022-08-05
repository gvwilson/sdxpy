import sys


def run_tests(prefix):
    """Run all the functions whose names start with the given prefix."""
    for name in [n for n in globals() if n.startswith(prefix)]:
        try:
            globals()[name]()
            print(f"pass: {name}")
        except AssertionError as e:
            print(f"fail: {name} {str(e)}")
        except Exception as e:
            print(f"error: {name} {str(e)}")


class Fake:
    """An object that can take the place of a callable."""
    def __init__(self, func=None, value=None):
        """Construct."""
        self.calls = []
        self.func = func
        self.value = value

    def __call__(self, *args, **kwargs):
        """Remember the call and return either the result of
        the function given to the constructor or a constant."""
        self.calls.append([args, kwargs])
        if self.func is not None:
            return self.func(*args, **kwargs)
        return self.value
        

def fixit(name, func=None, value=None):
    """Replace the thing named 'name'."""
    assert name in globals()
    fake = Fake(func, value)
    globals()[name] = fake
    return fake


def adder(a, b):
    """The function we're testing."""
    return a + b


def test_with_real_function():
    """Does the real function work?"""
    assert adder(2, 3) == 5


def test_with_fixed_return_value():
    """Can we return a constant instead?"""
    fixit("adder", value=99)
    assert adder(2, 3) == 99


def test_fake_records_calls():
    """Does the fake object record all calls?"""
    fake = fixit("adder", value=99)
    assert adder(2, 3) == 99
    assert adder(3, 4) == 99
    assert adder.calls == [[(2, 3), {}], [(3, 4), {}]]


def test_fake_calculates_result():
    """Can the fake object calculate a value?"""
    fixit("adder", func=lambda left, right: 10 * left + right)
    assert adder(2, 3) == 23


# Let's try them out.
run_tests("test_")

# ----------------------------------------------------------------------

# But at this point, `adder` isn't the original function.
assert adder(2, 3) != 5

# ----------------------------------------------------------------------

class ContextFake(Fake):
    """Now make it work as a context manager."""

    def __init__(self, name, func=None, value=None):
        """Construct."""
        super().__init__(func, value)
        self.name = name
        self.original = None

    def __enter__(self):
        """Replace the original function."""
        assert self.name in globals()
        self.original = globals()[self.name]
        globals()[self.name] = self
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Put everything back."""
        globals()[self.name] = self.original


def subber(a, b):
    """Another function to test."""
    return a - b


def check_no_lasting_effects():
    """Make sure the function goes back to working."""
    assert subber(2, 3) == -1
    with ContextFake("subber", value=1234) as fake:
        assert subber(2, 3) == 1234
        assert len(fake.calls) == 1
    assert subber(2, 3) == -1

# Let's try again.
run_tests("check_")

# And yes, the function is back in place.
assert subber(9, 5) == 4
