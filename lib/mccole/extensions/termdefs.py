"""Show terms defined in chapter."""

import ark
import ibis

from glossary import glossary_ref
import util


@ibis.filters.register("termdefs")
@util.timing
def termdefs(node):
    """Construct list of defined terms."""
    if (not node.slug) or (node.slug not in ark.site.config["chapters"]):
        return ""
    keys = ark.site.config["_terms_"].get(node.slug, None)
    if not keys:
        return ""
    lang = ark.site.config["lang"]
    glossary = {g["key"]: g for g in util.load_glossary()}
    terms = [_make_ref(node, glossary, lang, key) for key in sorted(keys)]
    terms = [t for t in terms if t is not None]
    terms = ", ".join(terms)
    return f'<p class="terms">{util.kind("defined")}: \n{terms}\n</p>'


def _make_ref(node, glossary, lang, key):
    try:
        return glossary_ref([key, glossary[key][lang]["term"]], {}, node)
    except KeyError:
        util.warn(f"Unknown glossary key {key} in {node.slug}")
        return None
