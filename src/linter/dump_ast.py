import ast
import sys

with open(sys.argv[1], "r") as reader:
    source = reader.read()

tree = ast.parse(source)
print(ast.dump(tree, indent=4))
