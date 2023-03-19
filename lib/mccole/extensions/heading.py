"""Headings and cross-references."""

import sys
from dataclasses import dataclass

import ibis
import ivy
import shortcodes
import util


@dataclass
class Heading:
    """Keep track of heading information."""

    fileslug: str = ""
    depth: int = 0
    title: str = ""
    slug: str = ""
    number: tuple = ()
    label: str = ""


@ivy.events.register(ivy.events.Event.INIT)
def collect():
    """Collect information from pages."""
    # Gather data.
    major = util.make_major()
    collected = {}
    ivy.nodes.root().walk(lambda node: _collect(node, major, collected))
    _number(collected, major)
    _flatten(collected)
    ivy.nodes.root().walk(_modify)
    _titles()


def _collect(node, major, collected):
    """Pull data from a single node."""
    # Home page is untitled.
    if node.slug not in major:
        return

    # Only collecting top-level chapters and appendices.
    if len(node.path) > 1:
        return

    # Use page metadata to create entry for level-1 heading.
    try:
        title = node.meta["title"]
    except KeyError:
        util.fail(f"No title in metadata of {node.filepath}")
    collected[node.slug] = [Heading(node.slug, 1, title, node.slug)]

    # Collect depth, text, and slug from each heading.
    collected[node.slug].extend(
        [
            Heading(node.slug, len(m.group(1)), m.group(2), m.group(4))
            for m in util.HEADING.finditer(node.text)
        ]
    )


def _number(headings, major):
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


def _flatten(collected):
    """Create flat cross-reference table."""
    headings = util.make_config("headings")
    for group in collected.values():
        for entry in group:
            headings[entry.slug] = entry


def _modify(node):
    """Post-processing changes."""
    node.text = util.HEADING.sub(_patch, node.text)
    headings = util.get_config("headings")
    if node.slug in headings:
        node.meta["major"] = util.make_label("part", headings[node.slug].number)


def _patch(match):
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


def _titles():
    """Create list of chapter/appendix titles for contents listing."""
    headings = util.get_config("headings")

    chapters = [headings[slug] for slug in ivy.site.config["chapters"]]
    for (i, entry) in enumerate(chapters):
        entry.label = str(i + 1)

    appendices = [headings[slug] for slug in ivy.site.config["appendices"]]
    for (i, entry) in enumerate(appendices):
        entry.label = chr(ord("A") + i)

    util.make_config("titles", {"chapters": chapters, "appendices": appendices})


# ----------------------------------------------------------------------


@shortcodes.register("x")
def heading_ref(pargs, kwargs, node):
    """Handle [%x slug %] section reference."""
    util.require(
        (len(pargs) == 1) and not kwargs, f"Bad 'x' shortcode {pargs} and {kwargs}"
    )
    headings = util.get_config("headings")
    slug = pargs[0]
    try:
        heading = headings[slug]
        label = util.make_label("part", heading.number)
        anchor = f"#{slug}" if (len(heading.number) > 1) else ""
        cls = 'class="x-ref"'
        return f'<a {cls} href="@root/{heading.fileslug}/{anchor}">{label}</a>'
    except KeyError:
        print(f"Unknown part cross-reference key {slug}", file=sys.stderr)
        return "FIXME"


@ibis.filters.register("part_name")
def part_name(slug):
    """Insert chapter/appendix part name."""
    headings = util.get_config("headings")
    util.require(slug in headings, f"Unknown slug for part name {slug}")
    entry = headings[slug]
    return f'{util.make_label("part", entry.number)}'
