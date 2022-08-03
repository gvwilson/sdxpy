"""Handle glossary references and glossary."""

import re
from pathlib import Path

import ivy
import shortcodes
import util
import yaml

# Regex to extract internal cross-references from bodies of definitions.
INTERNAL_REF = re.compile(r"\]\(#(.+?)\)")


@ivy.events.register(ivy.events.Event.INIT)
def glossary_collect():
    """Collect terms defined in each document."""
    if (filename := ivy.site.config.get("glossary", None)) is None:
        return '<p class="warning">No glossary specified.</p>'
    if (lang := ivy.site.config.get("lang", None)) is None:
        return '<p class="warning">No language specified.</p>'
    glossary = _read_glossary(filename)
    glossary = {item["key"]:item[lang]["term"] for item in glossary}

    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse_g, "g")
    defs = util.make_config("definitions")
    ivy.nodes.root().walk(lambda node: _parse_shortcodes(node, parser, defs, glossary))


@shortcodes.register("g")
def glossary_ref(pargs, kwargs, node):
    """Handle [% g slug "text" %] glossary reference shortcodes."""
    util.require((len(pargs) == 2) and (not kwargs), "Bad 'g' shortcode")
    slug = pargs[0]
    text = pargs[1]

    used = util.make_config("glossary")
    used.add(slug)
    return _format_ref(slug, text)


@shortcodes.register("glossary")
def glossary(pargs, kwargs, node):
    """Convert glossary to Markdown."""
    util.require((not pargs) and (not kwargs), "Bad 'glossary' shortcode")
    if (filename := ivy.site.config.get("glossary", None)) is None:
        return '<p class="warning">No glossary specified.</p>'
    if (lang := ivy.site.config.get("lang", None)) is None:
        return '<p class="warning">No language specified.</p>'

    glossary = _read_glossary(filename)
    try:
        glossary.sort(key=lambda x: x[lang]["term"].lower())
    except KeyError as exc:
        util.fail(f"Glossary entries missing key, term, or {lang}: {exc}.")

    entries = "\n\n".join(_as_markdown(glossary, lang, entry) for entry in glossary)
    return f'<div class="glossary" markdown="1">\n{entries}\n</div>'


@ivy.events.register(ivy.events.Event.EXIT)
def check():
    """Check that glossary entries are defined and used."""
    if (filename := ivy.site.config.get("glossary", None)) is None:
        return '<p class="warning">No glossary specified.</p>'
    if (lang := ivy.site.config.get("lang", None)) is None:
        util.fail("No language defined for glossary")

    glossary = _read_glossary(filename)
    defined = {entry["key"] for entry in glossary}

    if (used := util.get_config("glossary")) is None:
        return
    used |= _internal_references(glossary, lang)
    used |= _cross_references(glossary, lang)

    util.warn("unknown glossary references", used - defined)
    util.warn("unused glossary entries", defined - used)


def _as_markdown(glossary, lang, entry):
    """Convert a single glossary entry to Markdown."""
    cls = 'class="gl-key"'
    first = f'<span {cls} id="{entry["key"]}">{entry[lang]["term"]}</span>'

    if "acronym" in entry[lang]:
        first += f" ({entry[lang]['acronym']})"

    body = util.MULTISPACE.sub(entry[lang]["def"], " ").rstrip()

    if "ref" in entry[lang]:
        seealso = util.TRANSLATIONS[lang]["seealso"]
        try:
            refs = [f"[{glossary[r]}](#{r})" for r in entry[lang]["ref"]]
        except KeyError as exc:
            util.fail(f"Unknown glossary cross-ref key in {entry['key']}: {exc}")
        body += f"<br/>{seealso}: {', '.join(refs)}."

    result = f"{first}\n:   {body}"
    return result


def _cross_references(glossary, lang):
    """Get all explicit cross-references from glossary entries."""
    result = set()
    for entry in glossary:
        result.update(entry.get("ref", []))
    return result


def _format_ref(slug, text):
    """Format a glossary reference."""
    cls = 'class="gl-ref"'
    return f'<a {cls} href="@root/glossary/#{slug}" markdown="1">{text}</a>'


def _internal_references(glossary, lang):
    """Get all in-body cross-references from glossary entries."""
    result = set()
    for entry in glossary:
        for match in INTERNAL_REF.finditer(entry[lang]["def"]):
            result.add(match.group(1))
    return result


def _parse_shortcodes(node, parser, defs, glossary):
    """Collect information from node."""
    used = set()
    parser.parse(node.text, used)
    if not used:
        return
    terms = [(key, glossary[key]) for key in glossary if key in used]
    terms.sort(key=lambda item: item[1].lower())
    defs.append((node.slug, terms))


def _parse_g(pargs, kwargs, extra):
    """Collect information from a single glossary shortcode."""
    extra.add(pargs[0])
    return ""


def _read_glossary(filename):
    """Load the glossary definitions."""
    filename = Path(ivy.site.home(), filename)
    with open(filename, "r") as reader:
        return yaml.safe_load(reader) or {}
