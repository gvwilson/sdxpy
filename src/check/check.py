import sys
import yaml
from bs4 import BeautifulSoup, Tag
from visitor import Visitor


# [check]
class Check(Visitor):
    def __init__(self, manifest):
        self.manifest = manifest
        self.empty = set()
        self.problems = {}

    def _tag_enter(self, node):
        actual = {child.name for child in node
                  if isinstance(child, Tag)}
        errors = actual - self.manifest.get(node.name, self.empty)
        if errors:
            errors |= self.problems.get(node.name, set())
            self.problems[node.name] = errors
# [/check]


# [main]
def read_manifest(filename):
    with open(filename, "r") as reader:
        result = yaml.load(reader, Loader=yaml.FullLoader)
        for key in result:
            result[key] = set(result[key])
        return result

manifest = read_manifest(sys.argv[1])
with open(sys.argv[2], "r") as reader:
    text = reader.read()
doc = BeautifulSoup(text, "html.parser")

checker = Check(manifest)
checker.visit(doc.html)
for key, value in checker.problems.items():
    print(f"{key}: {', '.join(sorted(value))}")
# [/main]
