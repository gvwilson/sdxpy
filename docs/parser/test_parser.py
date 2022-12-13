from parser import parse

def test_parse_empty_string():
    assert parse("") == []

def test_parse_single_literal():
    assert parse("a") == [{"kind": "Lit", "loc": 0, "value": "a"}]

def test_parse_multiple_literals():
    assert parse("ab") == [
        {"kind": "Lit", "loc": 0, "value": "a"},
        {"kind": "Lit", "loc": 1, "value": "b"},
    ]

# [omit]
def test_parse_start_anchors():
    assert parse("^a") == [
        {"kind": "Start", "loc": 0},
        {"kind": "Lit", "loc": 1, "value": "a"},
    ]

def test_handles_circumflex_not_at_start():
    assert parse("a^") == [
        {"kind": "Lit", "loc": 0, "value": "a"},
        {"kind": "Lit", "loc": 1, "value": "^"},
    ]

def test_parse_end_anchors():
    assert parse("a$") == [
        {"kind": "Lit", "loc": 0, "value": "a"},
        {"kind": "End", "loc": 1},
    ]

def test_parse_circumflex_not_at_start():
    assert parse("$a") == [
        {"kind": "Lit", "loc": 0, "value": "$"},
        {"kind": "Lit", "loc": 1, "value": "a"},
    ]

def test_parse_empty_groups():
    assert parse("()") == [{"kind": "Group", "loc": 0, "end": 1, "children": []}]

def test_parse_groups_containing_characters():
    assert parse("(a)") == [
        {
            "kind": "Group",
            "loc": 0,
            "end": 2,
            "children": [{"kind": "Lit", "loc": 1, "value": "a"}],
        }
    ]

def test_parse_two_groups_containing_characters():
    assert parse("(a)(b)") == [
        {
            "kind": "Group",
            "loc": 0,
            "end": 2,
            "children": [{"kind": "Lit", "loc": 1, "value": "a"}],
        },
        {
            "kind": "Group",
            "loc": 3,
            "end": 5,
            "children": [{"kind": "Lit", "loc": 4, "value": "b"}],
        },
    ]

def test_parse_any():
    assert parse("a*") == [
        {"kind": "Any", "loc": 1, "child": {"kind": "Lit", "loc": 0, "value": "a"}}
    ]

def test_parse_any_of_group():
    assert parse("(ab)*") == [
        {
            "kind": "Any",
            "loc": 4,
            "child": {
                "kind": "Group",
                "loc": 0,
                "end": 3,
                "children": [
                    {"kind": "Lit", "loc": 1, "value": "a"},
                    {"kind": "Lit", "loc": 2, "value": "b"},
                ],
            },
        }
    ]

def test_parse_alt():
    assert parse("a|b") == [
        {
            "kind": "Alt",
            "loc": 1,
            "left": {"kind": "Lit", "loc": 0, "value": "a"},
            "right": {"kind": "Lit", "loc": 2, "value": "b"},
        }
    ]

def test_parse_alt_of_any():
    assert parse("a*|b") == [
        {
            "kind": "Alt",
            "loc": 2,
            "left": {
                "kind": "Any",
                "loc": 1,
                "child": {"kind": "Lit", "loc": 0, "value": "a"},
            },
            "right": {"kind": "Lit", "loc": 3, "value": "b"},
        }
    ]
# [/omit]

def test_parse_alt_of_groups():
    assert parse("a|(bc)") == [
        {
            "kind": "Alt",
            "loc": 1,
            "left": {"kind": "Lit", "loc": 0, "value": "a"},
            "right": {
                "kind": "Group",
                "loc": 2,
                "end": 5,
                "children": [
                    {"kind": "Lit", "loc": 3, "value": "b"},
                    {"kind": "Lit", "loc": 4, "value": "c"},
                ],
            },
        }
    ]
