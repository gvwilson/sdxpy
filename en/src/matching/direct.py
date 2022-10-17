# [base_class]
class MatchBase:
    def __init__(self):
        pass

    def match(self, text, start=0):
        return None
# [/base_class]

class Alt(MatchBase):
    def __init__(self, left, right):
        super().__init__()

class Any(MatchBase):
    def __init__(self, child):
        super().__init__()

class End(MatchBase):
    pass

# [lit]
class Lit(MatchBase):
    def __init__(self, chars):
        super().__init__()
        self.chars = chars

    def match(self, text, start=0):
        nextIndex = start + len(self.chars)
        if nextIndex > len(text):
            return None
        if text[start:nextIndex] != self.chars:
            return None
        return nextIndex
# [/lit]

class Seq(MatchBase):
    def __init__(self, *others):
        super().__init__()

class Start(MatchBase):
    pass

# [tests]
def main():
    tests = [
        ["a", "a", True, Lit("a")],
        ["b", "a", False, Lit("b")],
        ["a", "ab", True, Lit("a")],
        ["b", "ab", True, Lit("b")],
        ["ab", "ab", True, Seq(Lit("a"), Lit("b"))],
        ["ba", "ab", False, Seq(Lit("b"), Lit("a"))],
        ["ab", "ba", False, Lit("ab")],
        ["^a", "ab", True, Seq(Start(), Lit("a"))],
        ["^b", "ab", False, Seq(Start(), Lit("b"))],
        ["a$", "ab", False, Seq(Lit("a"), End())],
        ["a$", "ba", True, Seq(Lit("a"), End())],
        ["a*", "", True, Any("a")],
        ["a*", "baac", True, Any("a")],
        ["ab*c", "ac", True, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab*c", "abc", True, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab*c", "abbbc", True, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab*c", "abxc", False, Seq(Lit("a"), Any("b"), Lit("c"))],
        ["ab|cd", "xaby", True, Alt(Lit("ab"), Lit("cd"))],
        ["ab|cd", "acdc", True, Alt(Lit("ab"), Lit("cd"))],
        ["a(b|c)d", "xabdy", True, Seq(Lit("a"), Alt(Lit("b"), Lit("c")), Lit("d"))],
        ["a(b|c)d", "xabady", False, Seq(Lit("a"), Alt(Lit("b"), Lit("c")), Lit("d"))],
    ]
    for (pattern, text, expected, matcher) in tests:
        actual = matcher.match(text)
        result = "pass" if actual == expected else "fail"
        print(f"'{pattern}' X '{text}' == {actual}: {result}")
# [/tests]

if __name__ == "__main__":
    main()
