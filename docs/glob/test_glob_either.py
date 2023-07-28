from glob_lit import Lit
from glob_any import Any
from glob_either import Either

# [tests]
def test_either_two_literals_first():
    # /{a,b}/ matches "a"
    assert Either(Lit("a"), Lit("b")).match("a")

def test_either_two_literals_not_both():
    # /{a,b}/ doesn't match "ab"
    assert not Either(Lit("a"), Lit("b")).match("ab")
# [/tests]

def test_either_two_literals_second():
    # /{a,b}/ matches "b"
    assert Either(Lit("a"), Lit("b")).match("b")

def test_either_two_literals_neither():
    # /{a,b}/ doesn't match "c"
    assert not Either(Lit("a"), Lit("b")).match("c")

def test_either_after_any():
    # /*{x,y}/ matches "abcx"
    assert Any(Either(Lit("x"), Lit("y"))).match("abcx")

def test_either_leading_or_trailing():
    # /{*x,y*}/ matches "abx"
    # /{*x,y*}/ matches "yab"
    # /{*x,y*}/ matches "yabx"
    assert Either(Any(Lit("x")), Lit("y", Any())).match("abx")
    assert Either(Any(Lit("x")), Lit("y", Any())).match("yab")
    assert Either(Any(Lit("x")), Lit("y", Any())).match("yabx")
