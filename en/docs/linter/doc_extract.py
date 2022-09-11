"""Extract docstrings."""

import ast
from pathlib import Path
import sys


# [start]
class Extract(ast.NodeVisitor):
    """Extraction class."""

    @staticmethod
    def extract(filenames):
        """Entry-level method."""
        extracter = Extract()
        for filename in filenames:
            with open(filename, "r") as reader:
                source = reader.read()
                tree = ast.parse(source)
                module_name = Path(filename).stem
                extracter.extract_from(module_name, tree)
        return extracter.seen
# [/start]

    # [body]
    def __init__(self):
        """Constructor."""
        super().__init__()
        self.stack = []
        self.seen = {}

    def visit_ClassDef(self, node):
        """Get docstring from class."""
        self.save("class", node.name, node)
        self.generic_visit(node)
        self.stack.pop()

    def extract_from(self, module_name, tree):
        """Start extraction for a module."""
        self.save("module", module_name, tree)
        self.visit(tree)
        self.stack.pop()

    def save(self, kind, name, node):
        """Save information about a docstring."""
        self.stack.append(name)
        docstring = ast.get_docstring(node)
        self.seen[".".join(self.stack)] = (kind, docstring)
    # [/body]

    def visit_FunctionDef(self, node):
        """Get docstring from function."""
        self.save("function", node.name, node)
        self.generic_visit(node)
        self.stack.pop()


if __name__ == "__main__":
    results = Extract.extract(sys.argv[1:])
    for key, value in results.items():
        print(f"{key}: {value}")
