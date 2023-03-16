class Lit:
    def __init__(self, chars, rest=None):
        self.chars = chars
        self.rest = rest

    def match(self, text, start=0):
        end = start + len(self.chars)
        if text[start:end] != self.chars:
            return False
        if self.rest:
            return self.rest.match(text, end)
        return end == len(text)

class Any:
    def __init__(self, rest=None):
        self.rest = rest

    def match(self, text, start=0):
        if self.rest is None:
            return True
        for i in range(start, len(text)):
            if self.rest.match(text, i):
                return True
        return False

class Either:
    def __init__(self, left, right, rest=None):
        self.left = left
        self.right = right
        self.rest = rest

    def match(self, text, start=0):
        return self.left.match(text, start) or self.right.match(text, start)

def test_literal_match_entire_string():
    # 'abc' % "abc"
    assert Lit("abc").match("abc")

def test_literal_substring_alone_no_match():
    # 'ab' ! "abc"
    assert not Lit("ab").match("abc")

def test_literal_superstring_no_match():
    # 'abc' ! "ab"
    assert not Lit("abc").match("ab")

def test_star_matches_empty():
    # '*' % ""
    assert Any().match("")

def test_star_matches_entire_string():
    # '*' % "abc"
    assert Any().match("abc")

def test_star_matches_as_prefix():
    # '*def' % "abcdef"
    assert Any(Lit("def")).match("abcdef")

def test_star_matches_as_suffix():
    # 'abc*' % "abcdef"
    assert Lit("abc", Any()).match("abcdef")

def test_star_matches_interior():
    # 'a*c' % "abc"
    assert Lit("a", Any(Lit("c"))).match("abc")

def test_either_two_literals_first():
    # '{a,b}' % "a"
    assert Either(Lit("a"), Lit("b")).match("a")

def test_either_two_literals_second():
    # '{a,b}' % "b"
    assert Either(Lit("a"), Lit("b")).match("b")

def test_either_two_literals_neither():
    # '{a,b}' ! "c"
    assert not Either(Lit("a"), Lit("b")).match("c")

def test_either_two_literals_not_both():
    # '{a,b}' ! "ab"
    assert not Either(Lit("a"), Lit("b")).match("ab")

def test_either_after_any():
    # '*{x,y}' % "abcx"
    assert Any(Either(Lit("x"), Lit("y"))).match("abcx")

def test_either_leading_or_trailing():
    # '{*x,y*}' % "abx"
    # '{*x,y*}' % "yab"
    # '{*x,y*}' % "yabx"
    assert Either(Any(Lit("x")), Lit("y", Any())).match("abx")
    assert Either(Any(Lit("x")), Lit("y", Any())).match("yab")
    assert Either(Any(Lit("x")), Lit("y", Any())).match("yabx")
