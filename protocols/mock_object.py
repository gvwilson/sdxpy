from util import run_tests

# mccole:fake
class Fake:
    def __init__(self, func=None, value=None):
        self.calls = []
        self.func = func
        self.value = value

    def __call__(self, *args, **kwargs):
        self.calls.append([args, kwargs])
        if self.func is not None:
            return self.func(*args, **kwargs)
        return self.value
# mccole:/fake

# mccole:fakeit
def fakeit(name, func=None, value=None):
    assert name in globals()
    fake = Fake(func, value)
    globals()[name] = fake
    return fake
# mccole:/fakeit

# mccole:test_real
def adder(a, b):
    return a + b

def test_with_real_function():
    assert adder(2, 3) == 5
# mccole:/test_real

# mccole:test_fixed
def test_with_fixed_return_value():
    fakeit("adder", value=99)
    assert adder(2, 3) == 99
# mccole:/test_fixed

# mccole:test_record
def test_fake_records_calls():
    fake = fakeit("adder", value=99)
    assert adder(2, 3) == 99
    assert adder(3, 4) == 99
    assert adder.calls == [[(2, 3), {}], [(3, 4), {}]]
# mccole:/test_record

# mccole:test_calc
def test_fake_calculates_result():
    fakeit("adder", func=lambda left, right: 10 * left + right)
    assert adder(2, 3) == 23
# mccole:/test_calc

if __name__ == "__main__":
    run_tests(globals(), "test_")
    # mccole:polluted
    # But at this point, 'adder' isn't the original function.
    print(f"adder(2, 3) is now {adder(2, 3)}")
    # mccole:/polluted
