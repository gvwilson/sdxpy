# [match]
def match(pattern, text):
    if not pattern:
        return True

    # "^" at start of pattern matches start of text.
    if pattern[0] == "^":
        return match_here(pattern, 1, text, 0)

    # Try all possible starting points for pattern.
    # We need a do-while loop to handle the case of
    # matching an empty string.
    i_text = 0
    while True:
        if match_here(pattern, 0, text, i_text):
            return True
        i_text += 1
        if i_text == len(text):
            break

    # Nothing worked.
    return False


# [/match]

# [match_here]
def match_here(pattern, i_pattern, text, i_text):
    # There is no more pattern to match.
    if i_pattern == len(pattern):
        return True

    # "$" at end of pattern matches end of text.
    if (
        (i_pattern == (len(pattern) - 1))
        and (pattern[i_pattern] == "$")
        and (i_text == len(text))
    ):
        return True

    # "*" following current character means match many.
    if ((len(pattern) - i_pattern) > 1) and (pattern[i_pattern + 1] == "*"):
        while (i_text < len(text)) and (text[i_text] == pattern[i_pattern]):
            i_text += 1
        return match_here(pattern, i_pattern + 2, text, i_text)

    # There is no more text to match.
    if i_text == len(text):
        return False

    # Match a single character.
    if (pattern[i_pattern] == ".") or (pattern[i_pattern] == text[i_text]):
        return match_here(pattern, i_pattern + 1, text, i_text + 1)

    # Nothing worked.
    return False


# [/match_here]

# [tests]
def main():
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
        result = "pass" if actual == expected else "fail"
        print(f"'{regexp}' X '{text}' == {actual}: {result}")


main()
# [/tests]
