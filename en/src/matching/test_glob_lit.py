from glob_lit import Lit

def test_literal_match_entire_string():
    # ⌈abc⌋ ≈ "abc"
    assert Lit("abc").match("abc")

def test_literal_substring_alone_no_match():
    # ⌈ab⌋ ≉ "abc"
    assert not Lit("ab").match("abc")

def test_literal_superstring_no_match():
    # ⌈abc⌋ ≉ "ab"
    assert not Lit("abc").match("ab")
