from re_alt import Alt
from re_any import Any
from re_end import End
from re_lit import Lit
from re_start import Start


def main():
    tests = [
        ["a", "a", True, Lit("a")],
        ["b", "a", False, Lit("b")],
        ["a", "ab", True, Lit("a")],
        ["b", "ab", True, Lit("b")],
        ["ab", "ab", True, Lit("a", Lit("b"))],
        ["ba", "ab", False, Lit("b", Lit("a"))],
        ["ab", "ba", False, Lit("ab")],
        ["^a", "ab", True, Start(Lit("a"))],
        ["^b", "ab", False, Start(Lit("b"))],
        ["a$", "ab", False, Lit("a", End())],
        ["a$", "ba", True, Lit("a", End())],
        ["a*", "", True, Any(Lit("a"))],
        ["a*", "baac", True, Any(Lit("a"))],
        ["ab*c", "ac", True, Lit("a", Any(Lit("b"), Lit("c")))],
        ["ab*c", "abc", True, Lit("a", Any(Lit("b"), Lit("c")))],
        ["ab*c", "abbbc", True, Lit("a", Any(Lit("b"), Lit("c")))],
        ["ab*c", "abxc", False, Lit("a", Any(Lit("b"), Lit("c")))],
        ["ab|cd", "xaby", True, Alt(Lit("ab"), Lit("cd"))],
        ["ab|cd", "acdc", True, Alt(Lit("ab"), Lit("cd"))],
        ["a(b|c)d", "xabdy", True, Lit("a", Alt(Lit("b"), Lit("c"), Lit("d")))],
        ["a(b|c)d", "xabady", False, Lit("a", Alt(Lit("b"), Lit("c"), Lit("d")))],
    ]
    for (pattern, text, expected, matcher) in tests:
        actual = matcher.match(text)
        result = "pass" if actual == expected else "fail"
        print(f"'{pattern}' X '{text}' == {actual}: {result}")


if __name__ == "__main__":
    main()
