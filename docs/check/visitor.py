from bs4 import NavigableString, Tag

# [visitor]
class Visitor:
    def visit(self, node):
        if isinstance(node, NavigableString):
            self._text(node)
        elif isinstance(node, Tag):
            self._tag_enter(node)
            for child in node:
                self.visit(child)
            self._tag_exit(node)

    def _tag_enter(self, node): pass

    def _tag_exit(self, node): pass

    def _text(self, node): pass
# [/visitor]
