# [recurse]
def recurse(node):
    if isinstance(node, NavigableString):
        print(f"string: {repr(node.string)}")

    elif not isinstance(node, Tag):
        pass

    else:
        print(f"node: {node.name}")
        for child in node:
            recurse(child)
# [/recurse]

# [text]
text = """<html>
<body>
<h1>Title</h1>
<p>paragraph</p>
</body>
</html>"""
# [/text]

# [main]
from bs4 import BeautifulSoup, NavigableString, Tag

doc = BeautifulSoup(text, "html.parser")
recurse(doc)
# [/main]
