# [save]
# Tests to run.
HOPE_TESTS = []

# Record a single test for running later.
def hope_that(message, func):
    HOPE_TESTS.append([message, func])
# [/save]

# [main]
# Run all of the tests that have been asked for and report summary.
def main():
    results = {
        "pass": 0,
        "fail": 0,
        "error": 0
    }
    for [message, test] in HOPE_TESTS:
        try:
            test()
            results["pass"] += 1
        except AssertionError as exc:
            results["fail"] += 1
        except Exception as exc:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")
# [/main]

# [use]
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

# Register functions and Call the main driver.
hope_that("Sign of negative is -1", test_sign_negative)
hope_that("Sign of positive is 1", test_sign_positive)
hope_that("Sign of zero is 0", test_sign_zero)
hope_that("Sign misspelled is error", test_sign_error)
main()
# [/use]
