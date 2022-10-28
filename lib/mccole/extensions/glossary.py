"""Handle glossary references and glossary."""

import re

import ivy
import shortcodes
import util

# Regex to extract internal cross-references from bodies of definitions.
INTERNAL_REF = re.compile(r"\]\(#(.+?)\)")

# ----------------------------------------------------------------------

@ivy.events.register(ivy.events.Event.INIT)
def collect():
    """Collect information from pages."""
    major = util.make_major()
    collected = {}
    ivy.nodes.root().walk(lambda node: _collect(node, major, collected))
    _cleanup(collected)


def _collect(node, major, collected):
    """Pull data from a single node."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse, "g")
    temp = set()
    parser.parse(node.text, temp)
    collected[node.slug] = temp


def _parse(pargs, kwargs, data):
    """Collect information from a single glossary shortcode."""
    data.add(pargs[0])
    return ""


def _cleanup(collected):
    """Translate glossary definitions into required form."""
    filename = ivy.site.config.get("glossary", None)
    util.require(filename is not None, "No glossary specified")

    lang = ivy.site.config.get("lang", None)
    util.require(lang is not None, "No language specified")

    glossary = util.read_glossary(filename)
    glossary = {item["key"]: item[lang]["term"] for item in glossary}

    result = util.make_config("definitions")
    for (slug, seen) in collected.items():
        terms = [(key, glossary[key]) for key in glossary if key in seen]
        terms.sort(key=lambda item: item[1].lower())
        result.append((slug, terms))


# ----------------------------------------------------------------------

@shortcodes.register("g")
def glossary_ref(pargs, kwargs, node):
    """Handle [% g slug "text" %] glossary reference shortcodes."""
    util.require(
        (len(pargs) == 2) and (not kwargs), f"Bad 'g' shortcode {pargs} and {kwargs}"
    )
    slug = pargs[0]
    text = pargs[1]

    used = util.make_config("glossary")
    used.add(slug)
    return _format_ref(slug, text)


@shortcodes.register("glossary")
def glossary(pargs, kwargs, node):
    """Convert glossary to Markdown."""
    util.require(
        (not pargs) and (not kwargs), f"Bad 'glossary' shortcode {pargs} and {kwargs}"
    )

    filename = ivy.site.config.get("glossary", None)
    util.require(filename is not None, "No glossary specified")

    lang = ivy.site.config.get("lang", None)
    util.require(lang is not None, "No language specified")

    glossary = util.read_glossary(filename)
    try:
        glossary.sort(key=lambda x: x[lang]["term"].lower())
    except KeyError as exc:
        util.fail(f"Glossary entries missing key, term, or {lang}: {exc}.")

    markdown = [_as_markdown(glossary, lang, entry) for entry in glossary]
    entries = "\n\n".join(markdown)
    return f'<div class="glossary" markdown="1">\n{entries}\n</div>'


@ivy.events.register(ivy.events.Event.EXIT)
def check():
    """Check that glossary entries are defined and used."""
    filename = ivy.site.config.get("glossary", None)
    util.require(filename is not None, "No glossary specified")

    lang = ivy.site.config.get("lang", None)
    util.require(lang is not None, "No language defined for glossary")

    glossary = util.read_glossary(filename)
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
