# [match]
def match(pattern, text):
    # Empty pattern matches any string.
    if not pattern:
        return True

    # Start of string.
    if pattern[0] == "^":
        return match_here(pattern, 1, text, 0)

    # Need 'do-while' to handle zero characters matching.
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
    # No more pattern to match.
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
