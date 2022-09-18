from re_base import RegexBase


class Alt(RegexBase):
    def __init__(self, left, right, rest=None):
        super().__init__(rest)
        self.left = left
        self.right = right

    def _match(self, text, start):
        for pat in (self.left, self.right):
            after_pat = pat._match(text, start)
            if after_pat is not None:
                if not self.rest:
                    return after_pat
                after_rest = self.rest._match(text, after_pat)
                if after_rest is not None:
                    return after_rest
        return None
