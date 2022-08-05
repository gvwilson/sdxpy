from re_base import RegexBase

class Any(RegexBase):
    def __init__(self, child, rest=None):
        super().__init__(rest)
        self.child = child

    def _match(self, text, start):
        max_possible = len(text) - start
        for num in range(max_possible, -1, -1):
            after_many = self._match_many(text, start, num)
            if after_many is not None:
                return after_many
        return None

    def _match_many(self, text, start, num):
        for i in range(num):
            start = self.child._match(text, start)
            if start is None:
                return None
        if self.rest:
            return self.rest._match(text, start)
        return start
