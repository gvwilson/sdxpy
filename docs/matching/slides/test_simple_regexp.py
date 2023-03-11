from simple_regexp import match

def test_simple_regexp():
    tests = [
        ["", "", True],
        ["a", "a", True],
        ["b", "a", False],
        ["a", "ab", True],
        ["b", "ab", True],
        ["ab", "ba", False],
        ["^a", "ab", True],
        ["^b", "ab", False],
        ["a$", "ab", False],
        ["a$", "ba", True],
        ["a*", "", True],
        ["a*", "baac", True],
        ["ab*c", "ac", True],
        ["ab*c", "abc", True],
        ["ab*c", "abbbc", True],
        ["ab*c", "abxc", False],
    ]
    for (regexp, text, expected) in tests:
        actual = match(regexp, text)
        assert actual == expected
