from match import Either, Lit
from parser import Parser


class BetterParser(Parser):
    # [either]
    def _parse_EitherStart(self, rest, back):
        children = []
        while back and (back[0][0] == "Lit"):
            children.append(Lit(back[0][1]))
            back = back[1:]
        if not children:
            raise ValueError("empty Either")
        if back[0][0] != "EitherEnd":
            raise ValueError("badly-formatted Either")
        return Either(children, self._parse(back[1:]))
    # [/either]
