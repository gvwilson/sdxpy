def sign(value):
    if value < 0:
        return -1
    else:
        return 1

# [tests]
TEST_FAIL = "test:fail"
TEST_SKIP = "test:skip"

def test_sign_negative():
    "test:skip"
    assert sign(-3) == -1

def test_sign_positive():
    assert sign(19) == 1

def test_sign_zero():
    "test:fail"
    assert sign(0) == 0

def test_sign_error():
    """Expect an error."""
    assert sgn(1) == 1
# [/tests]

# [run]
def run_tests(prefix):
    prefixed_names = [n for n in globals() if n.startswith(prefix)]
    for name in prefixed_names:
        func = globals()[name]
        try:
            if func.__doc__ and TEST_SKIP in func.__doc__:
                print(f"skip: {name}")
            else:
                func()
                print(f"pass: {name}")
        except AssertionError as e:
            if TEST_FAIL in func.__doc__:
                print(f"pass (expected failure): {name}")
            else:
                print(f"fail: {name} {str(e)}")
        except Exception as e:
            doc = f"/{func.__doc__}" if func.__doc__ else ""
            print(f"error: {name}{doc} {str(e)}")

run_tests("test_")
# [/run]

