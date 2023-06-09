"""Create index and index references.

Index entries are created using `[% i "some" "key" %]...text...[% /i %]`.  Keys
can use `major!minor` notation to create subheadings (LaTeX-style).

If some text is in both the glossary and the index, wrap the index shortcode
around the glossary shortcode:

    [% i "some" %][% g key %]some text[% /g %][% /i %]

-   `index_ref` turns an index reference shortcode into text.

-   `make_index` displays the entire index.
"""

import ark
import shortcodes
import util


@ark.events.register(ark.events.Event.INIT)
def collect():
    """Collect information from pages."""
    major = util.make_major()
    collected = util.make_config("index")
    ark.nodes.root().walk(lambda node: _collect(node, major, collected))


def _collect(node, major, collected):
    """Pull data from a single node."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse, "i", "/i")
    temp = {"node": node, "index": collected}
    parser.parse(node.text, temp)


def _parse(pargs, kwargs, extra, content):
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


@shortcodes.register("i", "/i")
def index_ref(pargs, kwargs, node, content):
    """Handle [%i "some" "key" %]...text...[% /i %] index shortcodes."""
    util.require(pargs, f"Badly-formatted 'i' shortcode {pargs} in {node.filepath}")

    joined = ";".join(pargs)
    cls = 'class="ix-entry"'
    return f'<span {cls} ix-key="{joined}" markdown="1">{content}</span>'


@shortcodes.register("index")
def make_index(pargs, kwargs, node):
    """Handle [%index %] using saved data."""
    # No entries.
    if not (content := util.get_config("index")):
        return ""

    # Format multi-level list.
    result = ['<ul class="ix-list">']
    previous = None
    keys = list(content.keys())
    keys.sort(key=lambda x: tuple(y.lower() for y in x))
    for current in keys:
        occurrences = content[current]
        if len(current) == 1:
            links = _make_links(current[0], occurrences)
            result.append(f"<li>{current[0]}: {links}</li>")
            previous = current[0]
            continue

        util.require(
            len(current) == 2, f"Internal error index key '{current}' in {occurrences}"
        )

        if current[0] != previous:
            result.append(f"<li>{current[0]}</li>")
        links = _make_links(current[1], occurrences)
        result.append(f"<li>…{current[1]}: {links}</li>")

    result.append("</ul>")
    return "\n".join(result)


def _make_links(term, slugs):
    """Turn a set of node slugs into links."""
    # Too early in cycle.
    if not (headings := util.get_config("headings")):
        return ""

    # Match headings to slugs and format.
    paths = ["../" if not s else f"../{s}/" for s in slugs]
    titles = [headings[s].title for s in slugs]
    triples = list(zip(slugs, paths, titles))
    major = util.make_major()
    triples.sort(key=lambda x: str(major[x[0]]))
    result = ", ".join(
        f'<a class="ix-ref" ix-ref="{term}" href="{path}">{title}</a>'
        for (slug, path, title) in triples
    )
    return result
