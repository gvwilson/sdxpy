"""Report suspicious fonts in diagrams."""

import argparse
import re
from xml.dom import minidom

DEFAULT_SIZE = "14"
DEFAULT_FONT = "Helvetica"
PAT = {
    "font-family": re.compile(r"\bfont-family:\s*(.+?);"),
    "font-size": re.compile(r"\bfont-size:\s*(.+?);"),
}


def main():
    """Main driver."""
    options = parse_args()
    font_problems = []
    sizes = {}
    expected = expected_font(options)
    for filename in options.files:
        doc = minidom.parse(filename).documentElement
        size = get_size(doc)
        if size not in sizes:
            sizes[size] = set()
        sizes[size].add(filename)
        font_problems.extend(find_fonts(filename, doc, expected))

    for key in sorted(sizes.keys()):
        if (key[0] != "px") or (key[1] > options.width):
            print(f"{key}: {', '.join(sorted(sizes[key]))}")

    for problem in font_problems:
        print(problem)


def expected_font(options):
    """Figure out what font is expected."""
    return f"{options.fontfamily}:{options.fontsize}px"


def find_fonts(filename, doc, expected):
    """Find all fonts in document."""
    seen = recurse(doc, set())
    seen = {f"{entry[0]}:{entry[1]}" for entry in seen if entry[0] is not None}
    seen -= {expected}
    return [f"{filename}: {', '.join(sorted(seen))}" for s in seen]


def get_attr(node, name):
    """Get the font-size or font-family attribute."""
    result = None
    if node.hasAttribute(name):
        result = node.getAttribute(name)
    elif node.hasAttribute("style"):
        if m := PAT[name].match(node.getAttribute("style")):
            result = m.group(1)
    return result


def get_size(doc):
    """Get width and height of document."""
    result = (get_attr(doc, "width"), get_attr(doc, "height"))
    if result[0].endswith("mm"):
        result = ("mm", int(result[0][:-2]), int(result[1][:-2]))
    elif result[0].endswith("px"):
        result = ("px", int(result[0][:-2]), int(result[1][:-2]))
    elif result[0].endswith("pt"):
        result = ("pt", int(result[0][:-2]), int(result[1][:-2]))
    else:
        result = ("raw", int(result[0]), int(result[1]))
    return result


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs=argparse.REMAINDER, help="Files to check")
    parser.add_argument("--fontfamily", default=DEFAULT_FONT, help="Font family")
    parser.add_argument("--fontsize", default=DEFAULT_SIZE, help="Font size")
    parser.add_argument(
        "--width", type=int, default=0, help="Maximum width to allow in pixels"
    )
    return parser.parse_args()


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
