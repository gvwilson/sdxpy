# [equal]
class Match:
    def __init__(self, rest):
        self.rest = rest if rest else Null()

    def __eq__(self, other):
        return (other is not None) and (
            self.__class__ == other.__class__
        )


class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def __eq__(self, other):
        return super().__eq__(other) and (
            self.chars == other.chars
        )
# [/equal]


class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)


class Either(Match):
    def __init__(self, children, rest=None):
        super().__init__(rest)
        self.children = children

    def __eq__(self, other):
        return super().__eq__(other) and self.children.__eq__(
            other.children
        )


class Null(Match):
    def __init__(self):
        self.rest = None
