from tokenizer import tokenize

def test_tokenize_single_character():
    assert tokenize("a") == [{"kind": "Lit", "value": "a", "loc": 0}]

def test_tokenize_char_sequence():
    assert tokenize("ab") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "Lit", "value": "b", "loc": 1},
    ]

def test_tokenize_start_anchor_alone():
    assert tokenize("^") == [{"kind": "Start", "loc": 0}]

def test_tokenize_start_anchor_followed_by_characters():
    assert tokenize("^a") == [
        {"kind": "Start", "loc": 0},
        {"kind": "Lit", "value": "a", "loc": 1},
    ]

# [omit]
def test_tokenize_circumflex_not_at_start():
    assert tokenize("a^b") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "Lit", "value": "^", "loc": 1},
        {"kind": "Lit", "value": "b", "loc": 2},
    ]

def test_tokenize_start_anchor_alone():
    assert tokenize("$") == [{"kind": "End", "loc": 0}]

def test_tokenize_nd_anchor_preceded_by_characters():
    assert tokenize("a$") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "End", "loc": 1},
    ]

def test_tokenize_dollar_sign_not_at_end():
    assert tokenize("a$b") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "Lit", "value": "$", "loc": 1},
        {"kind": "Lit", "value": "b", "loc": 2},
    ]

def test_tokenize_repetition_alone():
    assert tokenize("*") == [{"kind": "Any", "loc": 0}]

def test_tokenize_repetition_in_string():
    assert tokenize("a*b") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "Any", "loc": 1},
        {"kind": "Lit", "value": "b", "loc": 2},
    ]

def test_tokenize_repetition_at_end_of_string():
    assert tokenize("a*") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "Any", "loc": 1},
    ]

def test_tokenize_alternation_alone():
    assert tokenize("|") == [{"kind": "Alt", "loc": 0}]

def test_tokenize_alternation_in_string():
    assert tokenize("a|b") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "Alt", "loc": 1},
        {"kind": "Lit", "value": "b", "loc": 2},
    ]

def test_tokenize_alternation_at_start_of_string():
    assert tokenize("|a") == [
        {"kind": "Alt", "loc": 0},
        {"kind": "Lit", "value": "a", "loc": 1},
    ]

def test_tokenize_start_of_group_alone():
    assert tokenize("(") == [{"kind": "GroupStart", "loc": 0}]

def test_tokenize_start_of_group_in_string():
    assert tokenize("a(b") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "GroupStart", "loc": 1},
        {"kind": "Lit", "value": "b", "loc": 2},
    ]

def test_tokenize_end_of_group_alone():
    assert tokenize(")") == [{"kind": "GroupEnd", "loc": 0}]

def test_tokenize_end_of_group_at_the_end_of_string():
    assert tokenize("a)") == [
        {"kind": "Lit", "value": "a", "loc": 0},
        {"kind": "GroupEnd", "loc": 1},
    ]
# [/omit]

def test_tokenize_complex_expression():
    assert tokenize("^a*(bcd|e^)*f$gh$") == [
        {"kind": "Start", "loc": 0},
        {"kind": "Lit", "loc": 1, "value": "a"},
        {"kind": "Any", "loc": 2},
        {"kind": "GroupStart", "loc": 3},
        {"kind": "Lit", "loc": 4, "value": "b"},
        {"kind": "Lit", "loc": 5, "value": "c"},
        {"kind": "Lit", "loc": 6, "value": "d"},
        {"kind": "Alt", "loc": 7},
        {"kind": "Lit", "loc": 8, "value": "e"},
        {"kind": "Lit", "loc": 9, "value": "^"},
        {"kind": "GroupEnd", "loc": 10},
        {"kind": "Any", "loc": 11},
        {"kind": "Lit", "loc": 12, "value": "f"},
        {"kind": "Lit", "loc": 13, "value": "$"},
        {"kind": "Lit", "loc": 14, "value": "g"},
        {"kind": "Lit", "loc": 15, "value": "h"},
        {"kind": "End", "loc": 16},
    ]
