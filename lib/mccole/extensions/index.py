"""Create index and index references.

Index entries are created using one of two forms:

-   `[%i "text" %]` uses `text` as both the key and the visible text

-   `[%i "key" "text" %]` uses a separate key and text

Either form can have an optional `url=link` field to wrap the visible text
in a hyperlink.  `link` must be a key in the `info/links.yml` file.

-   `index_ref` turns an index reference shortcode into text.

-   `make_index` displays the entire index.
"""

import ark
import regex
import shortcodes
import util


@ark.events.register(ark.events.Event.INIT)
def collect():
    """Collect information from pages."""
    major = util.make_major_numbering()
    collected = util.make_config("index")
    ark.nodes.root().walk(lambda node: _collect(node, major, collected))


def _collect(node, major, collected):
    """Pull data from a single node."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse, "i")
    temp = {"node": node, "index": collected}
    try:
        parser.parse(node.text, temp)
    except shortcodes.ShortcodeSyntaxError as exc:
        util.fail(f"%i shortcode parsing error in {node}: {exc}")


def _parse(pargs, kwargs, extra):
    """Gather information from a single index shortcode."""
    node = extra["node"]
    index = extra["index"]
    key, _, _ = _get_fields(node, pargs, kwargs)
    index.setdefault(key, set()).add(node.slug)


@shortcodes.register("i")
def index_ref(pargs, kwargs, node):
    """Format index shortcodes."""
    key, text, url = _get_fields(node, pargs, kwargs)
    cls = 'class="ix-entry"'
    content = f"[{text}][{url}]" if url else text
    return f'<span {cls} ix-key="{key}" markdown="1">{content}</span>'


def _get_fields(node, pargs, kwargs):
    """Extract key, text, and url from [%i ... %]."""
    if len(pargs) == 1:
        key = text = pargs[0]
    elif len(pargs) == 2:
        key, text = pargs
    else:
        util.fail(f"Badly-formatted index entry {pargs} in {node}")
    url = kwargs.get("url", None)
    return key, text, url


# ----------------------------------------------------------------------


@shortcodes.register("index")
def make_index(pargs, kwargs, node):
    """Handle [% index %] using saved data."""
    # No entries.
    if not (content := util.get_config("index")):
        return ""

    # Add glossary entries to index.
    glossary_in_chapter = util.get_config("glossary_in_chapter")
    for (slug, terms) in glossary_in_chapter:
        for (_, term) in terms:
            if term not in content:
                content[term] = set()
            content[term].add(slug)

    # Calculate order for index links.
    sequence = [
        *[slug for slug in ark.site.config["chapters"]],
        *[slug for slug in ark.site.config["appendices"]]
    ]
    ordering = {slug:i for (i, slug) in enumerate(sequence)}

    # Format index list.
    result = ['<ul class="ix-list">']
    for text, occurrences in sorted(content.items()):
        links = _make_links(text, occurrences, ordering)
        result.append(f"<li>{text}: {links}</li>")
    result.append("</ul>")
    return "\n".join(result)


def _make_links(term, slugs, ordering):
    """Turn a set of node slugs into links."""
    # Too early in cycle.
    if not (headings := util.get_config("headings")):
        return ""

    # Match headings to slugs and format.
    paths = ["@root/" if not s else f"@root/{s}/" for s in slugs]
    titles = [headings[s].title for s in slugs]
    triples = list(zip(slugs, paths, titles))
    triples.sort(key=lambda trip: ordering[trip[0]])

    result = ", ".join(
        f'<a class="ix-ref" ix-ref="{term}" href="{path}">{title}</a>'
        for (slug, path, title) in triples
    )
    return result
