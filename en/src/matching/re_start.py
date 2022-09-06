from re_base import RegexBase

class Start(RegexBase):
    def _match(self, text, start):
        if start != 0:
            return None
        if not self.rest:
            return 0
        return self.rest._match(text, start)
