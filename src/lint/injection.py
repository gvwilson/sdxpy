import ast
import sys


# [attach]
class BlankNodeVisitor(ast.NodeVisitor):
    pass

def print_name(self, node):
    print(node.id)

setattr(BlankNodeVisitor, "visit_Name", print_name)
# [/attach]

# [main]
with open(sys.argv[1], "r") as reader:
    source = reader.read()
tree = ast.parse(source)
finder = BlankNodeVisitor()
finder.visit(tree)
# [/main]
