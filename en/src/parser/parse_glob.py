import string

CHARS = set(string.ascii_letters + string.digits)

class Match:
    def __init__(self, rest):
        self.rest = rest if rest else Null()

    def __eq__(self, other):
        return (other is not None) and (self.__class__ == other.__class__)

class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)

class Either(Match):
    def __init__(self, left, right, rest=None):
        super().__init__(rest)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return super().__eq__(other) and self.left.__eq__(other.left) and self.right.__eq__(other.right)

class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def __eq__(self, other):
        return super().__eq__(other) and (self.chars == other.chars)

class Null(Match):
    def __init__(self):
        self.rest = None

class Tokenizer:
    def __init__(self):
        self._setup()

    def tok(self, text):
        self._setup()
        for ch in text:
            if ch == "*":
                self._add("Any")
            elif ch == "{":
                self._add("EitherStart")
            elif ch == ",":
                self._add(None)
            elif ch == "}":
                self._add("EitherEnd")
            elif ch in CHARS:
                self.current += ch
            else:
                raise NotImplementedError(f"what is '{ch}'?")
        self._add(None)
        return self.result

    def _setup(self):
        self.result = []
        self.current = ""

    def _add(self, thing):
        if len(self.current) > 0:
            self.result.append(["Lit", self.current])
            self.current = ""
        if thing is not None:
            self.result.append([thing])

class Parser:
    def __init__(self):
        pass

    def parse(self, text):
        tokens = Tokenizer().tok(text)
        return self._parse(tokens)

    def _parse(self, tokens):
        if not tokens:
            return Null()

        front, back = tokens[0], tokens[1:]
        kind = front[0]

        if kind == "Any":
            return Any(self._parse(back))

        elif kind == "EitherStart":
            if len(back) < 3 or (back[0][0] != "Lit") or (back[1][0] != "Lit") or (back[2][0] != "EitherEnd"):
                raise ValueError("badly-formatted Either")
            left = Lit(back[0][1])
            right = Lit(back[1][1])
            return Either(left, right, self._parse(back[3:]))

        elif kind == "Lit":
            return Lit(front[1], self._parse(back))

        else:
            raise NotImplementedError(f"what is '{kind}'?")

def test_tok_empty_string():
    assert Tokenizer().tok("") == []

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
    assert Tokenizer().tok("*abc*") == [["Any"], ["Lit", "abc"], ["Any"]]

def test_tok_lit_any_lit():
    assert Tokenizer().tok("abc*xyz") == [["Lit", "abc"], ["Any"], ["Lit", "xyz"]]

def test_tok_either_single_lit():
    assert Tokenizer().tok("{abc}") == [["EitherStart"], ["Lit", "abc"], ["EitherEnd"]]

def test_tok_either_two_lit():
    assert Tokenizer().tok("{abc,def}") == [["EitherStart"], ["Lit", "abc"], ["Lit", "def"], ["EitherEnd"]]

def test_tok_any_either():
    assert Tokenizer().tok("*{abc,def}") == [["Any"], ["EitherStart"], ["Lit", "abc"], ["Lit", "def"], ["EitherEnd"]]

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

def test_parse_either_two_lit():
    assert Parser().parse("{abc,def}") == Either(Lit("abc"), Lit("def"))

def test_parse_any_either():
    assert Parser().parse("*{abc,def}") == Any(Either(Lit("abc"), Lit("def")))

def test_parse_empty_string():
    assert Parser().parse("") == Null()
