from df_col import DfCol

def test_construct_with_single_value():
    df = DfCol(a=[1])
    assert df.get("a", 0) == 1

# [test_two_pairs]
def test_construct_with_two_pairs():
    df = DfCol(a=[1, 2], b=[3, 4])
    assert df.get("a", 0) == 1
    assert df.get("a", 1) == 2
    assert df.get("b", 0) == 3
    assert df.get("b", 1) == 4
# [/test_two_pairs]

def test_nrow():
    assert DfCol(a=[1, 2], b=[3, 4]).nrow() == 2

def test_ncol():
    assert DfCol(a=[1, 2], b=[3, 4]).ncol() == 2

def test_equality():
    left = DfCol(a=[1, 2], b=[3, 4])
    right = DfCol(b=[3, 4], a=[1, 2])
    assert left.eq(right) and right.eq(left)

def test_inequality():
    left = DfCol(a=[1, 2], b=[3, 4])
    assert not left.eq(DfCol(a=[1, 2]))
    assert not left.eq(DfCol(a=[1, 2], b=[1, 2]))

def test_select():
    df = DfCol(a=[1, 2], b=[3, 4])
    selected = df.select("a")
    assert selected.eq(DfCol(a=[1, 2]))

# [test_filter]
def test_filter():
    def odd(a, b):
        return (a % 2) == 1

    df = DfCol(a=[1, 2], b=[3, 4])
    assert df.filter(odd).eq(DfCol(a=[1], b=[3]))
# [/test_filter]
