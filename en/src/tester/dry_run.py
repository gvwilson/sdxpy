# [save]
HOPE_TESTS = []

def hope_that(func):
    HOPE_TESTS.append(func)
# [/save]

# [tests]
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

hope_that(test_sign_negative)
hope_that(test_sign_positive)
hope_that(test_sign_zero)
hope_that(test_sign_error)
# [/tests]

# [run_tests]
def run_tests():
    results = {"pass": 0, "fail": 0, "error": 0}
    for test in HOPE_TESTS:
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

run_tests()
# [/run_tests]
