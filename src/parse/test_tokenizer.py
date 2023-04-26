from tokenizer import Tokenizer

# [tests]
def test_tok_empty_string():
    assert Tokenizer().tok("") == []


def test_tok_any_either():
    assert Tokenizer().tok("*{abc,def}") == [
        ["Any"],
        ["EitherStart"],
        ["Lit", "abc"],
        ["Lit", "def"],
        ["EitherEnd"],
    ]
# [/tests]

def test_tok_lit_only():
    assert Tokenizer().tok("abc") == [["Lit", "abc"]]


def test_tok_any_only():
    assert Tokenizer().tok("*") == [["Any"]]


def test_tok_either_start_only():
    assert Tokenizer().tok("{") == [["EitherStart"]]


def test_tok_either_end_only():
    assert Tokenizer().tok("}") == [["EitherEnd"]]


def test_tok_any_lit():
    assert Tokenizer().tok("*abc") == [["Any"], ["Lit", "abc"]]


def test_tok_lit_any():
    assert Tokenizer().tok("abc*") == [["Lit", "abc"], ["Any"]]


def test_tok_any_lit_any():
    assert Tokenizer().tok("*abc*") == [
        ["Any"],
        ["Lit", "abc"],
        ["Any"],
    ]


def test_tok_lit_any_lit():
    assert Tokenizer().tok("abc*xyz") == [
        ["Lit", "abc"],
        ["Any"],
        ["Lit", "xyz"],
    ]


def test_tok_either_single_lit():
    assert Tokenizer().tok("{abc}") == [
        ["EitherStart"],
        ["Lit", "abc"],
        ["EitherEnd"],
    ]


def test_tok_either_two_lit():
    assert Tokenizer().tok("{abc,def}") == [
        ["EitherStart"],
        ["Lit", "abc"],
        ["Lit", "def"],
        ["EitherEnd"],
    ]
