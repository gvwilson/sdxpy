# [display]
def display(node):
    if isinstance(node, NavigableString):
        print(f"string: {repr(node.string)}")
        return
    else:
        print(f"node: {node.name}")
        for child in node:
            display(child)
# [/display]

# [text]
text = """<html>
<body>
<h1>Title</h1>
<p>paragraph</p>
</body>
</html>"""
# [/text]

# [main]
from bs4 import BeautifulSoup, NavigableString

doc = BeautifulSoup(text, "html.parser")
display(doc)
# [/main]
