from tokenizer import Tokenizer
from match import Any, Either, Lit, Null


# [simple]
class Parser:
    def parse(self, text):
        tokens = Tokenizer().tok(text)
        return self._parse(tokens)

    def _parse_Any(self, rest, back):
        return Any(self._parse(back))

    def _parse_Lit(self, rest, back):
        return Lit(rest[0], self._parse(back))

    # [/simple]

    # [parse]
    def _parse(self, tokens):
        if not tokens:
            return Null()

        front, back = tokens[0], tokens[1:]
        handler_name = f"_parse_{front[0]}"
        if not hasattr(self, handler_name):
            raise NotImplementedError(f"what is '{front}'")

        handler = getattr(self, handler_name)
        return handler(front[1:], back)

    # [/parse]

    # [either]
    def _parse_EitherStart(self, rest, back):
        if (
            len(back) < 3
            or (back[0][0] != "Lit")
            or (back[1][0] != "Lit")
            or (back[2][0] != "EitherEnd")
        ):
            raise ValueError("badly-formatted Either")
        left = Lit(back[0][1])
        right = Lit(back[1][1])
        return Either([left, right], self._parse(back[3:]))

    # [/either]
