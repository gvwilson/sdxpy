# [recurse]
def recurse(node):
    if isinstance(node, Tag):
        print(f"node: {node.name} {node.attrs}")
        for child in node:
            recurse(child)
# [/recurse]

# [text]
text = """<html lang="en">
<body class="outline narrow">
<p align="left" align="right">paragraph</p>
</body>
</html>"""
# [/text]

# [main]
from bs4 import BeautifulSoup, NavigableString, Tag

doc = BeautifulSoup(text, "html.parser")
recurse(doc)
# [/main]
