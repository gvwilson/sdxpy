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

# [main]
def find_tests(prefix):
    for (name, func) in globals().items():
        if name.startswith(prefix):
            print(name, func)

find_tests("test_")
# [/main]
