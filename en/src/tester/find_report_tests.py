def sign(value):
    if value < 0:
        return -1
    else:
        return 1

def test_sign_negative():
    assert sign(-3) == -1

def test_sign_positive():
    assert sign(19) == 1

def test_sign_zero():
    assert sign(0) == 0

def test_sign_error():
    assert sgn(1) == 1

# [runner]
def run_tests(prefix):
    for (name, func) in globals().items():
        if name.startswith(prefix):
            try:
                func()
                print(name, "passed")
            except AssertionError:
                print(name, "failed")
            except Exception:
                print(name, "had error")

run_tests("test_")
# [/runner]
