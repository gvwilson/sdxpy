import sys
from bs4 import BeautifulSoup, Tag

# [recurse]
def recurse(node, catalog):
    assert isinstance(node, Tag)

    if node.name not in catalog:
        catalog[node.name] = set()

    for child in node:
        if isinstance(child, Tag):
            catalog[node.name].add(child.name)
            recurse(child, catalog)

    return catalog
# [/recurse]

with open(sys.argv[1], "r") as reader:
    text = reader.read()
doc = BeautifulSoup(text, "html.parser")
catalog = recurse(doc.html, {})
for tag, contents in sorted(catalog.items()):
    print(f"{tag}: {', '.join(sorted(contents))}")
