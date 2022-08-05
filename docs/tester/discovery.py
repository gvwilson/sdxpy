# Something to test (doesn't handle zero properly).
def sign(value):
    if value < 0:
        return -1
    else:
        return 1


# These two should pass.
def test_sign_negative():
    assert sign(-3) == -1


def test_sign_positive():
    assert sign(19) == 1


# This one should fail.
def test_sign_zero():
    assert sign(0) == 0


# This one is an error (misspelled function).
def test_sign_error():
    assert sgn(1) == 1


def run_tests(prefix):
    """Run all the functions whose names start with the given prefix."""
    prefixed_names = [n for n in globals() if n.startswith(prefix)]
    for name in prefixed_names:
        func = globals()[name]
        try:
            func()
            print(f"pass: {name}")
        except AssertionError as e:
            print(f"fail: {name} {str(e)}")
        except Exception as e:
            print(f"error: {name} {str(e)}")


if __name__ == "__main__":
    run_tests("test_")
