"""Display index and regenerate dot files for visualizing syllabus."""

import argparse
import sys
import textwrap
from pathlib import Path

import graphviz
import shortcodes
import util

# Colors to use for node types.
COLORS = {
    "FLOW": "cornsilk",
    "SINK": "pink",
    "SOURCE": "aquamarine",
}

# Attributes for entire graph, nodes, and edges.
GRAPH_ATTR = {
    "rankdir": "LR",
}
NODE_ATTR = {
    "fontname": "Verdana",
    "fontsize": "8",
    "shape": "box",
    "style": "filled",
}
DEPENDENCY_ATTR = {}
ORDER_ATTR = {
    "arrowhead": "none",
    "style": "dashed",
}

# Width of node labels.
LABEL_WIDTH = 12


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)

    glossary = util.read_glossary(config.glossary)
    glossary = {key: glossary[key][config.lang]["term"] for key in glossary}

    prose = read_all_prose(config)
    index = find_index_terms(glossary, prose)
    inverted_index = invert_index(glossary, index)

    if options.display != "none":
        show_index(options.display, glossary, inverted_index)

    if options.output is not None:
        chapter_slugs = choose_chapter_slugs(config, options)
        depends = make_depends(chapter_slugs, glossary, index)
        write_dot(options, config, depends)


def add_dot_links(dot, depends):
    """Add inter-chapter links to graph."""
    for slug, others in depends.items():
        for other in others:
            if other != slug:
                dot.edge(other, slug, **DEPENDENCY_ATTR)


def add_dot_nodes(config, dot, depends):
    """Add chapter nodes to graph."""
    for slug in depends:
        color = choose_color(slug, depends)
        label = "<br/>".join(textwrap.wrap(config.chapters[slug], width=LABEL_WIDTH))
        dot.node(slug, label=f"<{label}>", color=color)


def check_glossary_definitions(found):
    """Check that each glossary term is defined only once."""
    problems = {term: slugs for (term, slugs) in found.items() if len(slugs) > 1}
    if problems:
        fail(f"Multiple definition(s): {problems}")


def choose_chapter_slugs(config, options):
    """Select chapters to display in graph."""
    skip = set(options.skip)
    return [slug for slug in config.chapters if slug not in skip]


def choose_color(slug, depends):
    """Choose a color for a node."""
    in_count = len(depends[slug])
    out_count = len(list(x for x in depends.values() if slug in x))
    if in_count > 0 and out_count > 0:
        return COLORS["FLOW"]
    if in_count == 0:
        return COLORS["SOURCE"]
    return COLORS["SINK"]


def fail(msg):
    """Report error and quit."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def find_index_terms(glossary, prose):
    """Find all index terms by chapter/appendix slug."""

    def _parse_to_set(parser, text):
        temp = set()
        parser.parse(text, temp)
        return temp

    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(lambda pargs, kwargs, keys: keys.add((pargs[0], True)), "g")
    parser.register(lambda pargs, kwargs, keys: keys.add((pargs[0], False)), "i")

    try:
        return {slug: _parse_to_set(parser, text) for (slug, text) in prose.items()}
    except shortcodes.ShortcodeSyntaxError as exc:
        fail(f"%i shortcode parsing error: {exc}")


def invert_index(glossary, index):
    """Convert slug:(word, in_glossary) to word:(slug, in_glossary)."""
    result = {}
    for slug, entries in index.items():
        for word, in_glossary in entries:
            if in_glossary:
                word = glossary[word]
            if word not in result:
                result[word] = []
            result[word].append((slug, in_glossary))
    return result


def make_depends(chapter_slugs, glossary, index):
    """Figure out which items depends on which."""
    index = {slug: entries for (slug, entries) in index.items() if entries}
    defined = {
        slug: set(glossary[e[0]] for e in entries if e[0] in glossary)
        for (slug, entries) in index.items()
    }
    indexed = {
        slug: set(e[0] for e in entries if e[0] not in glossary)
        for (slug, entries) in index.items()
    }
    depends = {
        i_slug: set(
            d_slug
            for (d_slug, d_terms) in defined.items()
            if i_terms.intersection(d_terms)
        )
        for (i_slug, i_terms) in indexed.items()
    }

    chapter_slugs = set(chapter_slugs)
    result = {
        i_slug: set(d_slug for d_slug in i_depends if d_slug in chapter_slugs)
        for (i_slug, i_depends) in depends.items()
        if i_slug in chapter_slugs
    }
    return result


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument(
        "--display",
        default="none",
        choices=["none", "plain", "problems"],
        help="How to print",
    )
    parser.add_argument("--output", default=None, help="Output file")
    parser.add_argument("--skip", nargs="+", default=[], help="Slugs to skip")
    return parser.parse_args()


def read_all_prose(config):
    """Read prose of all chapters and appendices for constructing full index."""
    return {
        slug: open(Path(config.src_dir, slug, "index.md"), "r").read()
        for slug in [*config.chapters.keys(), *config.appendices.keys()]
    }


def select_syllabus_chapters(options, config):
    """Select chapters to display in syllabus."""
    return {
        slug: title
        for slug, title in config.chapters.items()
        if slug not in options.skip
    }


def show_index(display, glossary, inverted_index):
    """Display index terms."""
    for term, entries in sorted(inverted_index.items()):
        entries = [
            f"+{slug}" if in_glossary else slug for (slug, in_glossary) in entries
        ]
        line = f"{term}: {', '.join(entries)}"
        if (display != "problems") or (("+" in line) and (": +" not in line)):
            print(line)


def write_dot(options, config, depends):
    """Save dot file."""
    dot = graphviz.Digraph(graph_attr=GRAPH_ATTR, node_attr=NODE_ATTR)
    add_dot_nodes(config, dot, depends)
    add_dot_links(dot, depends)
    if options.output == "-":
        print(dot.source)
    else:
        dot.save(options.output)


if __name__ == "__main__":
    main()
