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

def match_here(pattern, i_pattern, text, i_text):
    if no_more_pattern(pattern, i_pattern, text, i_text):
        return True

    if dollar_at_end_of_text(pattern, i_pattern, text, i_text):
        return True

    if supposed_to_match_many(pattern, i_pattern, text, i_text):
        next_i_text = match_many(pattern, i_pattern, text, i_text)
        return match_here(pattern, i_pattern + 2, text, next_i_text)

    if no_more_text_to_match(pattern, i_pattern, text, i_text):
        return False

    if match_single_character(pattern, i_pattern, text, i_text):
        return match_here(pattern, i_pattern + 1, text, i_text + 1)

    return False  # nothing worked

def no_more_pattern(pat, i_pat, text, i_text):
    return i_pat == len(pat)

def dollar_at_end_of_text(pat, i_pat, text, i_text):
    return (pat[i_pat] == "$") \
        and (i_pat == (len(pat) - 1)) \
        and (i_text == len(text))

def supposed_to_match_many(pat, i_pat, text, i_text):
    return ((len(pat) - i_pat) > 1) \
        and (pat[i_pat + 1] == "*")

def match_many(pat, i_pat, text, i_text):
    while (i_text < len(text)) and (text[i_text] == pat[i_pat]):
        i_text += 1
    return i_text

def no_more_text_to_match(pat, i_pat, text, i_text):
    return i_text == len(text)

def match_single_character(pat, i_pat, text, i_text):
    return (pat[i_pat] == ".") \
        or (pat[i_pat] == text[i_text])
