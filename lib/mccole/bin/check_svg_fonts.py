"""Report suspicious fonts in diagrams."""

import re
import sys
from xml.dom import minidom

EXPECTED = "Verdana:12px"
PAT = {
    "font-family": re.compile(r"\bfont-family:\s*(.+?);"),
    "font-size": re.compile(r"\bfont-size:\s*(.+?);"),
}


def main():
    """Main driver."""
    expected = {EXPECTED}
    for filename in sys.argv[1:]:
        seen = recurse(minidom.parse(filename).documentElement, set())
        seen = {f"{entry[0]}:{entry[1]}" for entry in seen if entry[0] is not None}
        seen -= expected
        if seen:
            print(filename, ", ".join(sorted(seen)))


def get_attr(node, name):
    """Get the font-size or font-family attribute."""
    result = None
    if node.hasAttribute(name):
        result = node.getAttribute(name)
    elif node.hasAttribute("style"):
        if m := PAT[name].match(node.getAttribute("style")):
            result = m.group(1)
    return result


def recurse(node, accum):
    """Recurse through all nodes in SVG."""
    if node.nodeType != node.ELEMENT_NODE:
        return
    accum.add((get_attr(node, "font-family"), get_attr(node, "font-size")))
    for child in node.childNodes:
        recurse(child, accum)
    return accum


if __name__ == "__main__":
    main()
