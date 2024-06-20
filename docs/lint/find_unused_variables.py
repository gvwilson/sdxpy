import ast
import sys
from collections import namedtuple

# [scope]
Scope = namedtuple("Scope", ["name", "load", "store"])
# [/scope]

# [class]
class FindUnusedVariables(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.stack = []

    def visit_Module(self, node):
        self.search("global", node)

    def visit_FunctionDef(self, node):
        self.search(node.name, node)
    # [/class]

    # [search]
    def search(self, name, node):
        self.stack.append(Scope(name, set(), set()))
        self.generic_visit(node)
        scope = self.stack.pop()
        self.check(scope)

    def check(self, scope):
        unused = scope.store - scope.load
        if unused:
            names = ", ".join(sorted(unused))
            print(f"unused in {scope.name}: {names}")
    # [/search]

    # [name]
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.stack[-1].load.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.stack[-1].store.add(node.id)
        else:
            assert False, "Unknown context"
        self.generic_visit(node)

    # [/name]


# [main]
with open(sys.argv[1], "r") as reader:
    source = reader.read()
tree = ast.parse(source)
finder = FindUnusedVariables()
finder.visit(tree)
# [/main]
