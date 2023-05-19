from match import Any, Either, Lit, Null
from parser import Parser


def test_parse_empty_string():
    assert Parser().parse("") == Null()


def test_parse_lit_only():
    assert Parser().parse("abc") == Lit("abc")


def test_parse_any_only():
    assert Parser().parse("*") == Any()


def test_parse_any_lit():
    assert Parser().parse("*abc") == Any(Lit("abc"))


def test_parse_lit_any():
    assert Parser().parse("abc*") == Lit("abc", Any())


def test_parse_any_lit_any():
    assert Parser().parse("*abc*") == Any(Lit("abc", Any()))


def test_parse_lit_any_lit():
    assert Parser().parse("abc*xyz") == Lit("abc", Any(Lit("xyz")))


# [sample]
def test_parse_either_two_lit():
    assert Parser().parse("{abc,def}") == Either(
        [Lit("abc"), Lit("def")]
    )
# [/sample]


def test_parse_any_either():
    assert Parser().parse("*{abc,def}") == Any(
        Either([Lit("abc"), Lit("def")])
    )
