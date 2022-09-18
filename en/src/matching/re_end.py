from re_base import RegexBase


class End(RegexBase):
    def _match(self, text, start):
        if start != len(text):
            return None
        if not self.rest:
            return len(text)
        return self.rest._match(text, start)
