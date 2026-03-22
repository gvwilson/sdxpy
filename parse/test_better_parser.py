from match import Any, Either, Lit, Null
from better_parser import BetterParser


def test_parse_empty_string():
    assert BetterParser().parse("") == Null()


def test_parse_lit_only():
    assert BetterParser().parse("abc") == Lit("abc")


def test_parse_any_only():
    assert BetterParser().parse("*") == Any()


def test_parse_any_lit():
    assert BetterParser().parse("*abc") == Any(Lit("abc"))


def test_parse_lit_any():
    assert BetterParser().parse("abc*") == Lit("abc", Any())


def test_parse_any_lit_any():
    assert BetterParser().parse("*abc*") == Any(Lit("abc", Any()))


def test_parse_lit_any_lit():
    assert BetterParser().parse("abc*xyz") == Lit(
        "abc", Any(Lit("xyz"))
    )


def test_parse_either_two_lit():
    assert BetterParser().parse("{abc,def}") == Either(
        [Lit("abc"), Lit("def")]
    )


def test_parse_any_either():
    assert BetterParser().parse("*{abc,def}") == Any(
        Either([Lit("abc"), Lit("def")])
    )


def test_parse_any_either_long():
    assert BetterParser().parse("*{abc,def,ghi,jkl}") == Any(
        Either([Lit("abc"), Lit("def"), Lit("ghi"), Lit("jkl")])
    )
