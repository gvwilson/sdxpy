# [equal]
class Match:
    def __init__(self, rest):
        self.rest = rest if rest else Null()

    def __eq__(self, other):
        return (other is not None) and (self.__class__ == other.__class__)


class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def __eq__(self, other):
        return super().__eq__(other) and (self.chars == other.chars)
# [/equal]


class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)


class Either(Match):
    def __init__(self, left, right, rest=None):
        super().__init__(rest)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and self.left.__eq__(other.left)
            and self.right.__eq__(other.right)
        )


class Null(Match):
    def __init__(self):
        self.rest = None
