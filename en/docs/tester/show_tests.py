def test_sign_negative():
    assert sign(-3) == -1


def test_sign_positive():
    assert sign(19) == 1


def test_sign_zero():
    assert sign(0) == 0


def test_sign_error():
    assert sgn(1) == 1


def show_tests():
    """Show all functions that start with 'test_'."""
    for name in globals():
        if name.startswith("test_"):
            print(name)


if __name__ == "__main__":
    show_tests()
