"""Headings and cross-references."""

from dataclasses import dataclass

import ark
import filters
import regex
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


@ark.events.register(ark.events.Event.INIT)
def collect():
    """Collect information from pages."""
    major = util.make_major_numbering()
    collected = {}
    ark.nodes.root().walk(lambda node: _collect(node, major, collected))
    _number(collected, major)
    _flatten(collected)
    ark.nodes.root().walk(_modify)
    _titles()


def _collect(node, major, collected):
    """Pull data from a single node."""
    # Home page is untitled.
    if filters.is_root(node):
        return

    # Only collecting top-level chapters and appendices.
    if len(node.path) > 1:
        return

    # Use page metadata to create entry for level-1 heading.
    title = util.get_title(node)
    collected[node.slug] = [Heading(node.slug, 1, title, node.slug)]

    # Collect depth, text, and slug from each heading.
    collected[node.slug].extend(
        [
            Heading(node.slug, len(m.group(1)), m.group(2), m.group(4))
            for m in regex.MARKDOWN_HEADING.finditer(node.text)
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
            elif depth == len(stack) + 1:
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
    # Don't process root index file.
    if filters.is_root(node):
        return
    node.text = regex.MARKDOWN_HEADING.sub(_patch, node.text)
    headings = util.get_config("headings")
    slug = util.get_chapter_slug(node)
    if slug in headings:
        node.meta["major"] = util.make_label("part", headings[slug].number)


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

    chapters = [headings[slug] for slug in ark.site.config["chapters"]]
    for i, entry in enumerate(chapters):
        entry.label = str(i + 1)

    appendices = [headings[slug] for slug in ark.site.config["appendices"]]
    for i, entry in enumerate(appendices):
        entry.label = chr(ord("A") + i)

    util.make_config("titles", {"chapters": chapters, "appendices": appendices})


# ----------------------------------------------------------------------


@shortcodes.register("x")
def heading_ref(pargs, kwargs, node):
    """Handle [%x key %] or [%x key title=true %] cross-reference."""
    util.require(
        len(pargs) == 1,
        f"Bad 'x' shortcode {pargs} and {kwargs} in {node}",
    )
    headings = util.get_config("headings")
    key = pargs[0]
    try:
        heading = headings[key]
        label = util.make_label("part", heading.number)
        anchor = f"#{key}" if (len(heading.number) > 1) else ""
        cls = 'class="x-ref"'
        title = f": {heading.title}" if kwargs.get("title", None) else ""
        return f'<a {cls} href="@root/{heading.fileslug}/{anchor}">{label}{title}</a>'
    except KeyError:
        util.fail(f"Unknown part cross-reference key {key} in {node}")
