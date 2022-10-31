def test_addition():
    assert 2 + 2 == 4

def test_multiplication():
    assert 3 * 3 == 9

def test_remainder():
    assert 15 % 4 == 0 # this is wrong

# [runner]
def run_tests():
    for (name, func) in globals().items():
        if name.startswith("test_"):
            try:
                func()
                print(func.__name__, "passed")
            except AssertionError:
                print(func.__name__, "failed")

run_tests()
# [/runner]
