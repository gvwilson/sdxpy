import pytest

from direct import Alt, Any, End, Lit, Seq, Start

TESTS = [
    ["a", "a", True, Lit("a")],
    ["b", "a", False, Lit("b")],
    ["a", "ab", True, Lit("a")],
    ["b", "ab", True, Lit("b")],
    ["ab", "ab", True, Seq(Lit("a"), Lit("b"))],
    ["ba", "ab", False, Seq(Lit("b"), Lit("a"))],
    ["ab", "ba", False, Lit("ab")],
    ["^a", "ab", True, Seq(Start(), Lit("a"))],
    ["^b", "ab", False, Seq(Start(), Lit("b"))],
    ["a$", "ab", False, Seq(Lit("a"), End())],
    ["a$", "ba", True, Seq(Lit("a"), End())],
    ["a*", "", True, Any("a")],
    ["a*", "baac", True, Any("a")],
    ["ab*c", "ac", True, Seq(Lit("a"), Any("b"), Lit("c"))],
    ["ab*c", "abc", True, Seq(Lit("a"), Any("b"), Lit("c"))],
    ["ab*c", "abbbc", True, Seq(Lit("a"), Any("b"), Lit("c"))],
    ["ab*c", "abxc", False, Seq(Lit("a"), Any("b"), Lit("c"))],
    ["ab|cd", "xaby", True, Alt(Lit("ab"), Lit("cd"))],
    ["ab|cd", "acdc", True, Alt(Lit("ab"), Lit("cd"))],
    ["a(b|c)d", "xabdy", True, Seq(Lit("a"), Alt(Lit("b"), Lit("c")), Lit("d"))],
    ["a(b|c)d", "xabady", False, Seq(Lit("a"), Alt(Lit("b"), Lit("c")), Lit("d"))],
]


@pytest.mark.parametrize("params", TESTS)
def test_direct(params):
    pattern, text, expected, matcher = params
    actual = matcher.match(text)
    assert actual == expected, f"{pattern} vs {text}"
