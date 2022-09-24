from dataclasses import dataclass

import ivy
import shortcodes
import util


@dataclass
class Figure:
    """Keep track of information about a figure."""

    node: ivy.nodes.Node = None
    fileslug: str = ""
    cls: str = ""
    slug: str = ""
    img: str = ""
    alt: str = ""
    caption: str = ""
    number: tuple = ()
    width: str = ""


@dataclass
class Heading:
    """Keep track of heading information."""

    fileslug: str = ""
    depth: int = 0
    title: str = ""
    slug: str = ""
    number: tuple = ()


@dataclass
class Table:
    """Keep track of information about a single table."""

    fileslug: str = ""
    slug: str = ""
    caption: str = ""
    number: tuple = ()


@ivy.events.register(ivy.events.Event.INIT)
def collect():
    """Collect information from pages."""
    # Gather data.
    major = util.make_major()
    data = {
        "definitions": {},
        "figures": {},
        "headings": {},
        "index": util.make_config("index"),
        "syllabus": {},
        "tables": {},
        "titles": {},
    }

    ivy.nodes.root().walk(lambda node: _node_collect(node, major, data))

    # Clean up data.
    _figures_cleanup(data["figures"])
    _headings_cleanup(data["headings"], major)
    _syllabus_cleanup(data["syllabus"])
    _tables_cleanup(data["tables"])
    _titles_cleanup(data["titles"])

    # Post-processing.
    ivy.nodes.root().walk(_node_modify)
    data["definitions"] = _glossary_cleanup(data["definitions"])


def _node_collect(node, major, data):
    """Pull data from a single node."""
    # Non-shortcodes.
    _headings_parse(node, major, data["headings"])
    _syllabus_parse(node, data["syllabus"])
    _tables_parse(node, data["tables"])
    _titles_parse(node, data["titles"])

    # Shortcodes.
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_figure_parse, "figure")
    parser.register(_glossary_parse, "g")
    parser.register(_index_parse, "i", "/i")

    data["node"] = node
    data["collected_figures"] = []
    data["collected_glossary"] = set()

    parser.parse(node.text, data)

    data["definitions"][node.slug] = data["collected_glossary"]
    data["figures"][node.slug] = data["collected_figures"]


def _node_modify(node):
    """Post-processing changes."""
    # Headings.
    node.text = util.HEADING.sub(_headings_patch, node.text)
    headings = util.get_config("headings")
    if node.slug in headings:
        node.meta["major"] = util.make_label("part", headings[node.slug].number)


# ----------------------------------------------------------------------
# Figures
# ----------------------------------------------------------------------


def _figures_cleanup(collected):
    """Convert collected figures information to flat lookup table."""
    major = util.make_major()
    figures = util.make_config("figures")
    for fileslug in collected:
        if fileslug in major:
            for (i, entry) in enumerate(collected[fileslug]):
                entry.fileslug = fileslug
                entry.number = (str(major[fileslug]), str(i + 1))
                figures[entry.slug] = entry


def _figure_parse(pargs, kwargs, data):
    """Collect information from a single figure shortcode."""
    data["collected_figures"].append(Figure(data["node"], **kwargs))
    return ""


# ----------------------------------------------------------------------
# Glossary
# ----------------------------------------------------------------------


def _glossary_cleanup(definitions):
    """Translate glossary definitions into required form."""
    filename = ivy.site.config.get("glossary", None)
    util.require(filename is not None, "No glossary specified")

    lang = ivy.site.config.get("lang", None)
    util.require(lang is not None, "No language specified")

    glossary = util.read_glossary(filename)
    glossary = {item["key"]: item[lang]["term"] for item in glossary}

    result = util.make_config("definitions")
    for (slug, seen) in definitions.items():
        terms = [(key, glossary[key]) for key in glossary if key in seen]
        terms.sort(key=lambda item: item[1].lower())
        result.append((slug, terms))


def _glossary_parse(pargs, kwargs, data):
    """Collect information from a single glossary shortcode."""
    data["collected_glossary"].add(pargs[0])
    return ""


# ----------------------------------------------------------------------
# Headings
# ----------------------------------------------------------------------


def _headings_cleanup(collected, major):
    """Clean up collected headings."""
    _headings_number(collected, major)
    _headings_flatten(collected)


def _headings_flatten(collected):
    """Create flat cross-reference table."""
    headings = util.make_config("headings")
    for group in collected.values():
        for entry in group:
            headings[entry.slug] = entry


def _headings_number(headings, major):
    """Calculate heading numberings."""
    for slug in major:
        stack = [major[slug]]
        for entry in headings[slug]:
            depth = entry.depth

            # Level-1 heading is already in the stack.
            if depth == 1:
                pass

            # Deeper heading, so extend stack.
            elif depth > len(stack):
                while len(stack) < depth:
                    stack.append(1)

            # Heading at the same level, so increment.
            elif depth == len(stack):
                stack[-1] += 1

            # Shallower heading, so shrink stack and increment.
            elif depth < len(stack):
                stack = stack[:depth]
                stack[-1] += 1

            # Record number as tuple of strings.
            entry.number = tuple(str(s) for s in stack)


def _headings_parse(node, major, headings):
    # Home page is untitled.
    if node.slug not in major:
        return

    # Use page metadata to create entry for level-1 heading.
    try:
        title = node.meta["title"]
    except KeyError:
        util.fail(f"No title in metadata of {node.filepath}")
    headings[node.slug] = [Heading(node.slug, 1, title, node.slug)]

    # Collect depth, text, and slug from each heading.
    headings[node.slug].extend(
        [
            Heading(node.slug, len(m.group(1)), m.group(2), m.group(4))
            for m in util.HEADING.finditer(node.text)
        ]
    )


def _headings_patch(match):
    """Modify a single heading."""
    headings = util.get_config("headings")
    prefix = match.group(1)
    text = match.group(2)
    attributes = match.group(3) or ""
    slug = match.group(4)

    if slug is None:
        return f"{prefix} {text} {attributes}".rstrip()
    else:
        label = util.make_label("part", headings[slug].number)
        return f"{prefix} {label}: {text} {attributes}"


# ----------------------------------------------------------------------
# Index
# ----------------------------------------------------------------------


def _index_parse(pargs, kwargs, extra, content):
    """Gather information from a single index shortcode."""
    node = extra["node"]
    index = extra["index"]

    util.require(pargs, f"Empty index key in {node.filepath}")

    for entry in [key.strip() for key in pargs]:
        entry = util.MULTISPACE.sub(" ", entry)
        entry = tuple(s.strip() for s in entry.split("!") if s.strip())
        util.require(
            1 <= len(entry) <= 2,
            f"Badly-formatted index key {entry} in {node.filepath}",
        )
        index.setdefault(entry, set()).add(node.slug)


# ----------------------------------------------------------------------
# Syllabus
# ----------------------------------------------------------------------


def _syllabus_cleanup(collected):
    syllabi = [
        (slug, collected[slug][0], collected[slug][1])
        for slug in ivy.site.config["chapters"]
        if slug in collected
    ]
    util.make_config("syllabus", syllabi)


def _syllabus_parse(node, info):
    if "syllabus" in node.meta:
        assert "title" in node.meta
        info[node.slug] = (node.meta["title"], node.meta.get("syllabus", []))


# ----------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------


def _tables_cleanup(collected):
    """Convert collected table information to flat lookup table."""
    major = util.make_major()
    tables = util.make_config("tables")
    for fileslug in collected:
        if fileslug in major:
            for (i, entry) in enumerate(collected[fileslug]):
                entry.number = (str(major[fileslug]), str(i + 1))
                tables[entry.slug] = entry


def _tables_parse(node, tables):
    """Collect table information."""
    tables[node.slug] = []
    for (i, match) in enumerate(util.TABLE.finditer(node.text)):
        caption = util.TABLE_CAPTION.search(match.group(0))
        util.require(
            caption is not None,
            "Table div '{match.group(0)}' without caption in {node.filepath}",
        )

        slug = util.TABLE_ID.search(match.group(0))
        util.require(
            slug is not None,
            f"Table div '{match.group(0)}' without ID in {node.filepath}",
        )

        tables[node.slug].append(
            Table(fileslug=node.slug, caption=caption.group(1), slug=slug.group(1))
        )


# ----------------------------------------------------------------------
# Titles
# ----------------------------------------------------------------------


def _titles_cleanup(collected):
    chapters = [(slug, collected[slug]) for slug in ivy.site.config["chapters"]]
    appendices = [(slug, collected[slug]) for slug in ivy.site.config["appendices"]]
    util.make_config("titles", {"chapters": chapters, "appendices": appendices})


def _titles_parse(node, info):
    if "title" in node.meta:
        info[node.slug] = node.meta["title"]
