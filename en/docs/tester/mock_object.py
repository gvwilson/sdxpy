from util import run_tests


# [fake]
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


# [/fake]


# [fixit]
def fixit(name, func=None, value=None):
    """Replace the thing named 'name'."""
    assert name in globals()
    fake = Fake(func, value)
    globals()[name] = fake
    return fake


# [/fixit]


# [test_real]
def adder(a, b):
    """The function we're testing."""
    return a + b


def test_with_real_function():
    """Does the real function work?"""
    assert adder(2, 3) == 5


# [/test_real]


# [test_fixed]
def test_with_fixed_return_value():
    """Can we return a constant instead?"""
    fixit("adder", value=99)
    assert adder(2, 3) == 99


# [/test_fixed]


# [test_record]
def test_fake_records_calls():
    """Does the fake object record all calls?"""
    fake = fixit("adder", value=99)
    assert adder(2, 3) == 99
    assert adder(3, 4) == 99
    assert adder.calls == [[(2, 3), {}], [(3, 4), {}]]


# [/test_record]


# [test_calc]
def test_fake_calculates_result():
    """Can the fake object calculate a value?"""
    fixit("adder", func=lambda left, right: 10 * left + right)
    assert adder(2, 3) == 23


# [/test_calc]


if __name__ == "__main__":
    run_tests(globals(), "test_")
    # [polluted]
    # But at this point, `adder` isn't the original function.
    print(f"adder(2, 3) is now {adder(2, 3)}")
    # [/polluted]
