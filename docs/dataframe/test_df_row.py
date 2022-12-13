from df_row import DfRow

# [fixture]
def odd_even():
    return DfRow([{"a": 1, "b": 3}, {"a": 2, "b": 4}])

def a_only():
    return DfRow([{"a": 1}, {"a": 2}])
# [/fixture]

def test_construct_with_single_value():
    df = DfRow([{"a": 1}])
    assert df.get("a", 0) == 1

# [test_two_pairs]
def test_construct_with_two_pairs():
    df = odd_even()
    assert df.get("a", 0) == 1
    assert df.get("a", 1) == 2
    assert df.get("b", 0) == 3
    assert df.get("b", 1) == 4
# [/test_two_pairs]

def test_nrow():
    df = odd_even()
    assert df.nrow() == 2

def test_ncol():
    df = odd_even()
    assert df.ncol() == 2

def test_equality():
    left = odd_even()
    right = DfRow([{"a": 1, "b": 3}, {"a": 2, "b": 4}])
    assert left.eq(right) and right.eq(left)

def test_inequality():
    assert not odd_even().eq(a_only())
    repeated = DfRow([{"a": 1, "b": 3}, {"a": 1, "b": 3}])
    assert not odd_even().eq(repeated)

def test_select():
    selected = odd_even().select("a")
    assert selected.eq(a_only())

def test_filter():
    def odd(a, b):
        return (a % 2) == 1

    df = odd_even()
    assert df.filter(odd).eq(DfRow([{"a": 1, "b": 3}]))
