"""Create index and index references.

Index entries are created using `[% i "some" "key" %]...text...[% /i %]`.  Keys
can use `major!minor` notation to create subheadings (LaTeX-style).

If some text is in both the glossary and the index, wrap the index shortcode
around the glossary shortcode:

    [% i "some" %][% g key %]some text[% /g %][% /i %]

-   `index_ref` turns an index reference shortcode into text.

-   `make_index` displays the entire index.
"""

import shortcodes

import util


@shortcodes.register("i", "/i")
def index_ref(pargs, kwargs, node, content):
    """Handle [% i "some" "key" %]...text...[% /i %] index shortcodes."""
    # Badly formatted.
    if len(pargs) == 0:
        util.fail(f"Badly-formatted 'i' shortcode {pargs} in {node.filepath}")

    # Format.
    joined = ";".join(pargs)
    cls = 'class="ix-entry"'
    return f'<span {cls} ix-key="{joined}" markdown="1">{content}</span>'


@shortcodes.register("index")
def make_index(pargs, kwargs, node):
    """Handle [% index %] using saved data."""
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
        elif len(current) != 2:
            util.fail(f"Internal error index key '{current}' in {occurrences}")
        else:
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
