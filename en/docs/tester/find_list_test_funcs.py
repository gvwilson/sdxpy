def test_addition():
    assert 2 + 2 == 4

def test_multiplication():
    assert 3 * 3 == 9

def test_remainder():
    assert 15 % 4 == 0 # this is wrong

def find_tests():
    result = []
    for (name, func) in globals().items():
        if name.startswith("test_"):
            result.append(func)
    return result

print("all the test functions", find_tests())
