import string

# [class]
CHARS = set(string.ascii_letters + string.digits)

class Tokenizer:
    def __init__(self):
        self._setup()

    def _setup(self):
        self.result = []
        self.current = ""
# [/class]

    # [tok]
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
    # [/tok]

    # [add]
    def _add(self, thing):
        if len(self.current) > 0:
            self.result.append(["Lit", self.current])
            self.current = ""
        if thing is not None:
            self.result.append([thing])
    # [/add]
