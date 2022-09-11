import ast
from collections import Counter, namedtuple
import sys

# [class]
Handler = namedtuple("Handler", ["func", "data"])

class RegisterNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.handlers = {}

    def add_handler(self, nodeType, func, data=None):
        handler = Handler(func, data)
        if nodeType not in self.handlers:
            self.handlers[nodeType] = []
        self.handlers[nodeType].append(handler)

    def visit_Name(self, node):
        for handler in self.handlers.get(ast.Name, []):
            handler.func(node, handler.data)
# [/class]

# [handler]
def count_names(node, counter):
    counter[node.id] += 1
# [/handler]

# [main]
with open(sys.argv[1], "r") as reader:
    source = reader.read()
tree = ast.parse(source)

finder = RegisterNodeVisitor()
counter = Counter()
finder.add_handler(ast.Name, count_names, counter)

finder.visit(tree)
print(counter)
# [/main]
