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
