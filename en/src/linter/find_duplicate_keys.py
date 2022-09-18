import ast
import sys
from collections import Counter


# [class]
class FindDuplicateKeys(ast.NodeVisitor):
    def __init__(self):
        super().__init__()

    def visit_Dict(self, node):
        seen = Counter()
        for key in node.keys:
            if isinstance(key, ast.Constant):
                seen[key.value] += 1
        problems = {k for (k, v) in seen.items() if v > 1}
        self.report(node, problems)
        self.generic_visit(node)

    def report(self, node, problems):
        if problems:
            msg = ", ".join(p for p in problems)
            print(f"duplicate key(s) {{{msg}}} at line {node.lineno}")


# [/class]


with open(sys.argv[1], "r") as reader:
    source = reader.read()
tree = ast.parse(source)
finder = FindDuplicateKeys()
finder.visit(tree)
