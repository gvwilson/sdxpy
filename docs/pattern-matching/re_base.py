class RegexBase:
    def __init__(self, rest=None):
        self.rest = rest

    def match(self, text):
        for i in range(len(text) + 1):
            if self._match(text, i) is not None:
                return True
        return False

    def _match(self, text, start):
        raise NotImplementedError("derived classes must override '_match'")
