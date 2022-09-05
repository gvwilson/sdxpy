from dataclasses import dataclass

import ivy
import shortcodes

import util


@dataclass
class Figure:
    """Keep track of information about a figure."""

    node: ivy.nodes.Node = None
    fileslug: str = ""
    slug: str = ""
    img: str = ""
    alt: str = ""
    caption: str = ""
    number: tuple = ()
    width: str = ""


@ivy.events.register(ivy.events.Event.INIT)
def figures_collect():
    """Collect information by parsing shortcodes."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_figure_parse, "figure")
    figures = {}
    ivy.nodes.root().walk(lambda node: _figures_parse_shortcodes(node, parser, figures))
    _figures_flatten(figures)


def _figures_parse_shortcodes(node, parser, figures):
    """Collect information from node."""
    extra = {"node": node, "seen": []}
    parser.parse(node.text, extra)
    figures[node.slug] = extra["seen"]


def _figure_parse(pargs, kwargs, extra):
    """Collect information from a single figure shortcode."""
    extra["seen"].append(Figure(extra["node"], **kwargs))
    return ""


def _figures_flatten(collected):
    """Convert collected figures information to flat lookup table."""
    major = util.make_major()
    figures = util.make_config("figures")
    for fileslug in collected:
        if fileslug in major:
            for (i, entry) in enumerate(collected[fileslug]):
                entry.fileslug = fileslug
                entry.number = (str(major[fileslug]), str(i + 1))
                figures[entry.slug] = entry


# ----------------------------------------------------------------------


@ivy.events.register(ivy.events.Event.INIT)
def glossary_collect():
    """Collect terms defined in each document."""
    if (filename := ivy.site.config.get("glossary", None)) is None:
        return '<p class="warning">No glossary specified.</p>'
    if (lang := ivy.site.config.get("lang", None)) is None:
        return '<p class="warning">No language specified.</p>'
    glossary = util.read_glossary(filename)
    glossary = {item["key"]: item[lang]["term"] for item in glossary}

    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_glossary_parse_entry, "g")
    defs = util.make_config("definitions")
    ivy.nodes.root().walk(
        lambda node: _glossary_parse_shortcodes(node, parser, defs, glossary)
    )


def _glossary_parse_shortcodes(node, parser, defs, glossary):
    """Collect information from node."""
    used = set()
    parser.parse(node.text, used)
    if not used:
        return
    terms = [(key, glossary[key]) for key in glossary if key in used]
    terms.sort(key=lambda item: item[1].lower())
    defs.append((node.slug, terms))


def _glossary_parse_entry(pargs, kwargs, extra):
    """Collect information from a single glossary shortcode."""
    extra.add(pargs[0])
    return ""


# ----------------------------------------------------------------------


@dataclass
class Heading:
    """Keep track of heading information."""

    fileslug: str = ""
    depth: int = 0
    title: str = ""
    slug: str = ""
    number: tuple = ()


@ivy.events.register(ivy.events.Event.INIT)
def headings_collect():
    """Collect heading information using regular expressions."""
    major = util.make_major()
    headings = {}
    ivy.nodes.root().walk(lambda node: _headings_parse(node, major, headings))

    _headings_number(major, headings)
    _headings_flatten(headings)
    ivy.nodes.root().walk(_headings_modify)


def _headings_flatten(collected):
    """Create flat cross-reference table."""
    headings = util.make_config("headings")
    for group in collected.values():
        for entry in group:
            headings[entry.slug] = entry


def _headings_modify(node):
    node.text = util.HEADING.sub(_headings_patch, node.text)
    headings = util.get_config("headings")
    if node.slug in headings:
        node.meta["major"] = util.make_label("part", headings[node.slug].number)


def _headings_number(major, headings):
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


@ivy.events.register(ivy.events.Event.INIT)
def index_collect():
    """Collect information by parsing shortcodes."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_index_process, "i", "/i")
    index = util.make_config("index")
    ivy.nodes.root().walk(
        lambda node: parser.parse(node.text, {"node": node, "index": index})
    )


def _index_process(pargs, kwargs, extra, content):
    """Gather information from a single index shortcode."""
    node = extra["node"]
    index = extra["index"]

    if not pargs:
        util.fail(f"Empty index key in {node.filepath}")

    for entry in [key.strip() for key in pargs]:
        entry = util.MULTISPACE.sub(" ", entry)
        entry = tuple(s.strip() for s in entry.split("!") if s.strip())
        if 1 <= len(entry) <= 2:
            index.setdefault(entry, set()).add(node.slug)
        else:
            util.fail(f"Badly-formatted index key {entry} in {node.filepath}")


# ----------------------------------------------------------------------


@ivy.events.register(ivy.events.Event.INIT)
def syllabus_collect():
    """Collect chapter syllabi."""
    info = {}
    ivy.nodes.root().walk(lambda node: _syllabus_collect(info, node))
    syllabi = [
        (slug, info[slug][0], info[slug][1])
        for slug in ivy.site.config["chapters"]
        if slug in info
    ]
    util.make_config("syllabus", syllabi)


def _syllabus_collect(info, node):
    if "syllabus" in node.meta:
        assert "title" in node.meta
        info[node.slug] = (node.meta["title"], node.meta.get("syllabus", []))


# ----------------------------------------------------------------------


@dataclass
class Table:
    """Keep track of information about a single table."""

    fileslug: str = ""
    slug: str = ""
    caption: str = ""
    number: tuple = ()


@ivy.events.register(ivy.events.Event.INIT)
def tables_collect():
    """Collect table information using regular expressions."""
    tables = {}
    ivy.nodes.root().walk(lambda node: _tables_process(node, tables))
    _tables_flatten(tables)


def _tables_process(node, tables):
    """Collect table information."""
    tables[node.slug] = []
    for (i, match) in enumerate(util.TABLE.finditer(node.text)):
        if (caption := util.TABLE_CAPTION.search(match.group(0))) is None:
            util.fail(
                f"Table div '{match.group(0)}' without caption in {node.filepath}"
            )
        if (slug := util.TABLE_ID.search(match.group(0))) is None:
            util.fail(f"Table div '{match.group(0)}' without ID in {node.filepath}")
        tables[node.slug].append(
            Table(fileslug=node.slug, caption=caption.group(1), slug=slug.group(1))
        )


def _tables_flatten(collected):
    """Convert collected table information to flat lookup table."""
    major = util.make_major()
    tables = util.make_config("tables")
    for fileslug in collected:
        if fileslug in major:
            for (i, entry) in enumerate(collected[fileslug]):
                entry.number = (str(major[fileslug]), str(i + 1))
                tables[entry.slug] = entry


# ----------------------------------------------------------------------


@ivy.events.register(ivy.events.Event.INIT)
def titles_collect():
    """Collect page titles."""
    info = {}
    ivy.nodes.root().walk(lambda node: _titles_collect(info, node))
    chapters = [(slug, info[slug]) for slug in ivy.site.config["chapters"]]
    appendices = [(slug, info[slug]) for slug in ivy.site.config["appendices"]]
    util.make_config(
        "titles",
        {"chapters": chapters, "appendices": appendices}
    )


def _titles_collect(info, node):
    if "title" in node.meta:
        info[node.slug] = node.meta["title"]
