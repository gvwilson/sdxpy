# [display]
def display(node):
    if isinstance(node, Tag):
        print(f"node: {node.name} {node.attrs}")
        for child in node:
            display(child)
# [/display]

# [text]
text = """<html lang="en">
<body class="outline narrow">
<p align="left" align="right">paragraph</p>
</body>
</html>"""
# [/text]

# [main]
from bs4 import BeautifulSoup, Tag

doc = BeautifulSoup(text, "html.parser")
display(doc)
# [/main]
