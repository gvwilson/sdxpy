"""Handle index shortcode and create index."""

import ark
import shortcodes

import util


@shortcodes.register("i")
@util.timing
def index_ref(pargs, kwargs, node):
    """Format index shortcode."""
    if len(pargs) == 1:
        key = text = pargs[0]
    elif len(pargs) == 2:
        key, text = pargs
    else:
        util.fail(f"Badly-formatted index entry {pargs} in {node}")
    url = kwargs.get("url", None)
    cls = 'class="ix-entry"'
    content = f"[{text}][{url}]" if url else text
    return f'<span {cls} ix-key="{key}" markdown="1">{content}</span>'


@shortcodes.register("index")
@util.timing
def make_index(pargs, kwargs, node):
    """Handle [% index %] using saved data."""

    util.require(
        "_index_" in ark.site.config,
        "No index information has been added to site configuration",
    )

    # Calculate reference order for index links.
    all_slugs = ark.site.config["chapters"] + ark.site.config["appendices"]
    ordering = {slug: i for i, slug in enumerate(all_slugs)}

    # Construct full index.
    lookup = _invert_index()
    _add_glossary_to_index(lookup)

    # Format.
    keys = sorted(lookup.keys(), key=lambda x: x.lower())
    links = (_make_links(term, lookup[term], ordering) for term in keys)
    return "\n".join([
        '<ul class="ix-list">',
        *links,
        "</ul>",
    ])


def _add_glossary_to_index(lookup):
    """Add glossary entries to lookup table."""
    lang = ark.site.config["lang"]
    inverted = {entry["key"]: entry for entry in util.load_glossary()}
    for (slug, keys) in ark.site.config["_terms_"].items():
        for k in keys:
            t = inverted[k][lang]["term"]
            if t not in lookup:
                lookup[t] = set()
            lookup[t].add(slug)


def _invert_index():
    """Invert collected slug-to-term data."""
    lookup = {}
    for (slug, terms) in ark.site.config["_index_"].items():
        for t in terms:
            if t not in lookup:
                lookup[t] = set()
            lookup[t].add(slug)
    return lookup


def _make_links(key, slugs, ordering):
    """Turn a set of node slugs into links."""
    metadata = ark.site.config["_meta_"]
    paths = [f"@root/{s}/" for s in slugs]
    titles = [metadata[s]["title"] for s in slugs]
    triples = list(zip(slugs, paths, titles))
    triples.sort(key=lambda t: ordering[t[0]])
    result = ", ".join(
        f'<a class="ix-ref" ix-ref="{key}" href="{path}">{title}</a>'
        for (slug, path, title) in triples
    )
    if "!" in key:
        key = f"…{key.split('!')[-1]}"
    return f"<li>{key}: {result}</li>"
