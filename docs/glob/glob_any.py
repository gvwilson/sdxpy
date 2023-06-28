class Any:
    def __init__(self, rest=None):
        self.rest = rest

    def match(self, text, start=0):
        if self.rest is None:
            return True
        for i in range(start, len(text)):
            if self.rest.match(text, i):
                return True
        return False
