"""Build GraphViz file showing chapter dependencies."""

from pathlib import Path
import argparse
import frontmatter
import graphviz
import sys
import textwrap
import util

# Colors to use for node types.
COLORS = {
    "FLOW": "cornsilk",
    "SINK": "pink",
    "SOURCE": "aquamarine",
}

# Attributes for entire graph, nodes, and edges.
GRAPH_ATTRIBUTES = {
    "rankdir": "LR",
}
NODE_ATTRIBUTES = {
    "fontname": "Verdana",
    "fontsize": "8",
    "shape": "box",
    "style": "filled",
}
DEPENDENCY_ATTRIBUTES = {
}
ORDER_ATTRIBUTES = {
    "arrowhead": "none",
    "style": "dashed",
}

# Width of node labels.
LABEL_WIDTH = 12

# Output formats.
FORMATS = ["pdf", "png", "svg"]

def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    chapters = make_chapters(options, config)
    check_chapters(chapters)
    dot = graphviz.Digraph(graph_attr=GRAPH_ATTRIBUTES, node_attr=NODE_ATTRIBUTES)
    make_nodes(dot, chapters)
    make_dependency_links(dot, chapters)
    for fmt in FORMATS:
        dot.render(format=fmt, outfile=f"{options.output}_regular.{fmt}")
    make_order_links(dot, chapters)
    for fmt in FORMATS:
        dot.render(format=fmt, outfile=f"{options.output}_linear.{fmt}")


def check_chapters(chapters):
    """Check input validity."""
    good = True
    keys = set(chapters.keys())

    for slug, data in chapters.items():
        unknown = data["depends"] - keys
        if unknown:
            print(f"{slug}: unknown {', '.join(sorted(unknown))}", file=sys.stderr)
            good = False

    ordering = {slug:i for i, slug in enumerate(chapters.keys())}
    for i, slug in enumerate(chapters.keys()):
        out_of_order = {other for other in chapters[slug]["depends"] if ordering[other] > ordering[slug]}
        if out_of_order:
            print(f"{slug}: out of order {', '.join(sorted(out_of_order))}", file=sys.stderr)
            good = False

    if not good:
        sys.exit(1)


def get_info(config, slug):
    """Get information from a chapter."""
    with open(Path(config.src_dir, slug, "index.md"), "r") as reader:
        result = frontmatter.load(reader)
        assert "depends" in result, f"{slug} missing 'depends'"
        return set(result["depends"]) if result["depends"] else set()


def make_chapters(options, config):
    """Make data structure representing chapters."""
    chapters = {slug: title for slug, title in config.chapters.items() if slug not in options.skip}
    for slug, title in chapters.items():
        chapters[slug] = {"title": title, "depends": get_info(config, slug)}
    return chapters


def make_dependency_links(dot, chapters):
    """Make dependency links."""
    for slug, data in chapters.items():
        for other in data["depends"]:
            dot.edge(other, slug, **DEPENDENCY_ATTRIBUTES)


def make_nodes(dot, chapters):
    """Make chapter nodes."""
    for slug, data in chapters.items():
        in_count = len(data["depends"])
        out_count = len(list(x for x in chapters.values() if slug in x["depends"]))
        if in_count > 0 and out_count > 0:
            color = COLORS["FLOW"]
        elif in_count == 0:
            color = COLORS["SOURCE"]
        else:
            color = COLORS["SINK"]
        label = "<br/>".join(textwrap.wrap(data["title"], width=LABEL_WIDTH))
        dot.node(slug, label=f"<{label}>", color=color)


def make_order_links(dot, chapters):
    """Make ordering links."""
    ordered = list(chapters.keys())
    for i, slug in enumerate(ordered):
        if i == 0:
            continue
        dot.edge(ordered[i-1], slug, **ORDER_ATTRIBUTES)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--skip", nargs="+", default=[], help="Slugs to skip")
    parser.add_argument("--output", required=False, default=None, help="Output file (default stdout)")
    return parser.parse_args()
    

if __name__ == "__main__":
    main()
