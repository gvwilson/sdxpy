from glob_lit import Lit
from glob_any import Any

def test_any_matches_empty():
    # ⌈*⌋ ≈ ""
    assert Any().match("")

def test_any_matches_entire_string():
    # ⌈*⌋ ≈ "abc"
    assert Any().match("abc")

def test_any_matches_as_prefix():
    # ⌈*def⌋ ≈ "abcdef"
    assert Any(Lit("def")).match("abcdef")

def test_any_matches_as_suffix():
    # ⌈abc*⌋ ≈ "abcdef"
    assert Lit("abc", Any()).match("abcdef")

def test_any_matches_interior():
    # ⌈a*c⌋ ≈ "abc"
    assert Lit("a", Any(Lit("c"))).match("abc")
