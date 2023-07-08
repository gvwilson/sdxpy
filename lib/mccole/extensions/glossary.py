"""Handle glossary references and glossary."""

import html
import re
import ark
import regex
import shortcodes
import util


UNMARKDOWN = [
    (regex.MULTISPACE, " "),
    (re.compile(r"\[(.+?)\]\(.+?\)"), lambda match: match.group(1)),
]


@ark.events.register(ark.events.Event.INIT)
def collect():
    """Collect information from pages."""
    major = util.make_major()
    collected = {}
    ark.nodes.root().walk(lambda node: _collect(node, major, collected))
    _cleanup(collected)


def _collect(node, major, collected):
    """Pull data from a single node."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse, "g")
    temp = set()
    try:
        parser.parse(node.text, temp)
    except shortcodes.ShortcodeSyntaxError as exc:
        util.fail(f"%g shortcode parsing error in {node.filepath}: {exc}")
    collected[node.slug] = temp


def _parse(pargs, kwargs, data):
    """Collect information from a single glossary shortcode."""
    data.add(pargs[0])
    return ""


def _cleanup(collected):
    """Save glossary terms to show definitions per chapter."""
    _, _ = util.read_glossary()  # to ensure load
    glossary = util.get_config("glossary_by_key")
    used = util.make_config("glossary_in_chapter")
    for slug, seen in collected.items():
        terms = [(key, glossary[key]["term"]) for key in glossary if key in seen]
        terms.sort(key=lambda item: item[1].lower())
        used.append((slug, terms))


# ----------------------------------------------------------------------


@shortcodes.register("g")
def glossary_ref(pargs, kwargs, node):
    """Handle [% g slug "text" %] glossary reference shortcodes."""
    util.require(
        (len(pargs) == 2) and (not kwargs), f"Bad 'g' shortcode {pargs} and {kwargs}"
    )
    key, text = pargs
    used = util.make_config("glossary_keys_used")
    used.add(key)
    return _format_ref(key, text)


@shortcodes.register("glossary")
def glossary(pargs, kwargs, node):
    """Convert glossary to Markdown."""
    util.require(
        (not pargs) and (not kwargs), f"Bad 'glossary' shortcode {pargs} and {kwargs}"
    )
    glossary, lang = util.read_glossary()
    try:
        glossary.sort(key=lambda x: x[lang]["term"].lower())
    except KeyError as exc:
        util.fail(f"Glossary entries missing key, term, or {lang}: {exc}.")

    markdown = [_as_markdown(entry, lang) for entry in glossary]
    entries = "\n\n".join(markdown)
    return f'<div class="glossary" markdown="1">\n{entries}\n</div>'


@ark.events.register(ark.events.Event.EXIT)
def check():
    """Check that glossary entries are defined and used."""
    glossary, lang = util.read_glossary()
    defined = {entry["key"] for entry in glossary}

    if (used := util.get_config("glossary_keys_used")) is None:
        return
    used |= _internal_references(glossary, lang)
    used |= _cross_references(glossary, lang)

    util.warn("unknown glossary references", used - defined)
    util.warn("unused glossary entries", defined - used)


def _as_markdown(entry, lang):
    """Convert a single glossary entry to Markdown."""
    cls = 'class="gl-key"'
    first = f'<span {cls} id="{entry["key"]}">{entry[lang]["term"]}</span>'

    if "acronym" in entry[lang]:
        first += f" ({entry[lang]['acronym']})"
    elif "full" in entry[lang]:
        first += f" ({entry[lang]['full']})"

    body = regex.MULTISPACE.sub(entry[lang]["def"], " ").rstrip()

    if "ref" in entry:
        glossary = util.get_config("glossary_by_key")
        seealso = util.TRANSLATIONS[lang]["seealso"]
        try:
            refs = [f"[{glossary[r]['term']}](#{r})" for r in entry["ref"]]
        except KeyError as exc:
            util.fail(f"Unknown glossary cross-ref in {entry['key']}: {exc}")
        body += f"<br/>{seealso}: {', '.join(refs)}."

    result = f"{first}\n:   {body}"
    return result


def _cross_references(glossary, lang):
    """Get all explicit cross-references from glossary entries."""
    result = set()
    for entry in glossary:
        result.update(entry.get("ref", []))
    return result


def _format_ref(key, text):
    """Format a glossary reference."""
    cls = 'class="gl-ref"'
    href = f'href="@root/glossary/#{key}"'
    tooltip = f'title="{_make_tooltip(key)}"'
    return f'<a {cls} {href} {tooltip} markdown="1">{text}</a>'


def _internal_references(glossary, lang):
    """Get all in-body cross-references from glossary entries."""
    result = set()
    for entry in glossary:
        for match in regex.GLOSSARY_INTERNAL_REF.finditer(entry[lang]["def"]):
            result.add(match.group(1))
    return result


def _make_tooltip(key):
    """Make tooltip for glossary display."""
    glossary = util.get_config("glossary_by_key")
    util.require(key in glossary, f"Unknown glossary key {key}")
    entry = glossary[key]
    text = entry["def"].strip()
    for (pat, sub) in UNMARKDOWN:
        text = pat.sub(sub, text)
    return html.escape(text)
