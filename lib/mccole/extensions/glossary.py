"""Handle glossary references and glossary."""

import ark
import re
import shortcodes

import util


# Scrub whitespace.
WHITESPACE = re.compile(r'\s', re.DOTALL)


@shortcodes.register("g")
@util.timing
def glossary_ref(pargs, kwargs, node):
    """Handle [%g key "text" %] glossary reference shortcode."""
    util.require(
        (len(pargs) == 2) and (not kwargs),
        f"Bad 'g' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    key, text = pargs
    cls = 'class="gl-ref"'
    href = f'href="@root/glossary/#{key}"'
    return f'<a {cls} {href} markdown="1">{text}</a>'


@shortcodes.register("glossary")
@util.timing
def glossary(pargs, kwargs, node):
    """Handle [% glossary %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'glossary' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    lang = ark.site.config["lang"]
    glossary = util.load_glossary()

    try:
        glossary.sort(key=lambda x: x[lang]["term"].lower())
    except KeyError as exc:
        util.fail(f"Glossary entries missing key, term, or {lang}: {exc}.")

    inverted = {entry["key"]: entry for entry in glossary}
    combined = "\n\n".join([_as_markdown(inverted, entry, lang) for entry in glossary])
    return util.markdownify(combined).replace("<dl>", '<dl class="glossary">', 1)


def _as_markdown(inverted, entry, lang):
    """Convert a single glossary entry to Markdown."""
    key = entry["key"]
    term = entry[lang]["term"]
    acronym = f" ({entry[lang]['acronym']})" if "acronym" in entry[lang] else ""
    defn = WHITESPACE.sub(' ', entry[lang]["def"]) + _add_see_also(inverted, entry, lang)
    return f'{term}{acronym} {{: #{key}}}\n:   {defn}'


def _add_see_also(inverted, entry, lang):
    """Add 'see also' if present."""
    if "ref" not in entry:
        return ""
    try:
        refs = [f"[{inverted[r][lang]['term']}](#{r})" for r in entry["ref"]]
    except KeyError as exc:
        util.fail(f"Unknown glossary cross-ref in {entry['key']}: {exc}")
    return f" See also: {', '.join(refs)}."
