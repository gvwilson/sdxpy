import ast
from pathlib import Path
import sys


class Extract(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.seen = {}

    def extract(self, module_name, tree):
        self.save(module_name, tree)
        self.visit(tree)
        self.stack.pop()

    def visit_ClassDef(self, node):
        self.save(node.name, node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node):
        self.save(node.name, node)
        self.generic_visit(node)
        self.stack.pop()

    def save(self, name, node):
        self.stack.append(name)
        self.seen[".".join(self.stack)] = ast.get_docstring(node)


def main():
    extracter = Extract()
    for filename in sys.argv[1:]:
        with open(filename, "r") as reader:
            source = reader.read()
            tree = ast.parse(source)
            module_name = Path(filename).stem
            extracter.extract(module_name, tree)
    for key, value in extracter.seen.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
