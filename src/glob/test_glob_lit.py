from glob_lit import Lit

# [tests]
def test_literal_match_entire_string():
    # ⌈abc⌋ ≈ "abc"
    assert Lit("abc").match("abc")

def test_literal_substring_alone_no_match():
    # ⌈ab⌋ ≉ "abc"
    assert not Lit("ab").match("abc")

def test_literal_superstring_no_match():
    # ⌈abc⌋ ≉ "ab"
    assert not Lit("abc").match("ab")
# [/tests]

# [chain]
def test_literal_followed_by_literal_match():
    # ⌈a⌋⌈b⌋ ≈ "ab"
    assert Lit("a", Lit("b")).match("ab")

def test_literal_followed_by_literal_no_match():
    # ⌈a⌋⌈b⌋ ≉ "ac"
    assert not Lit("a", Lit("b")).match("ac")
# [/chain]
