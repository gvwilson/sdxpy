# mccole:display
def display(node):
    if isinstance(node, Tag):
        print(f"node: {node.name} {node.attrs}")
        for child in node:
            display(child)
# mccole:/display

# mccole:text
text = """<html lang="en">
<body class="outline narrow">
<p align="left" align="right">paragraph</p>
</body>
</html>"""
# mccole:/text

# mccole:main
from bs4 import BeautifulSoup, Tag

doc = BeautifulSoup(text, "html.parser")
display(doc)
# mccole:/main
