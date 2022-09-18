from re_base import RegexBase


class Lit(RegexBase):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def _match(self, text, start):
        next_index = start + len(self.chars)
        if next_index > len(text):
            return None
        if text[start:next_index] != self.chars:
            return None
        if not self.rest:
            return next_index
        return self.rest._match(text, next_index)
