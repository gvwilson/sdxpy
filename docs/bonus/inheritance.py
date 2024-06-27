import ast
import sys


# [init]
class FindClassesAndMethods(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.parents = {}
        self.methods = {}

    # [/init]

    # [classdef]
    def visit_ClassDef(self, node):
        class_name = node.name
        assert class_name not in self.methods
        self.stack.append(class_name)
        self.methods[class_name] = set()
        self.parents[class_name] = {p.id for p in node.bases}
        self.generic_visit(node)
        self.stack.pop()

    # [/classdef]

    # [methoddef]
    def visit_FunctionDef(self, node):
        if not self.stack:
            return
        class_name = self.stack[-1]
        assert class_name in self.methods
        method_name = node.name
        assert method_name not in self.methods[class_name]
        self.methods[class_name].add(method_name)

    # [/methoddef]

    def report(self, stream):
        assert set(self.methods.keys()) == set(self.parents.keys())
        all_classes = sorted(self.methods.keys())
        all_methods = set()
        for v in self.methods.values():
            all_methods |= v
        all_methods = sorted(all_methods)
        print(f"| | {' | '.join(all_classes)} |")
        print(f"|{'|'.join([' --- '] * (len(all_classes) + 1))}|")
        for m in all_methods:
            defined = ["X" if m in self.methods[c] else " " for c in all_classes]
            print(f"| {m} | {' | '.join(defined)}")


def main():
    collector = FindClassesAndMethods()
    for filename in sys.argv[1:]:
        with open(filename, "r") as reader:
            source = reader.read()
            tree = ast.parse(source)
            collector.visit(tree)
    collector.report(sys.stdout)


if __name__ == "__main__":
    main()
