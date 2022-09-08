"""Generate bibliography."""

from pathlib import Path

import ivy
import shortcodes
import util
from pybtex.database import parse_file
from pybtex.plugin import find_plugin


@shortcodes.register("b")
def bibliography_ref(pargs, kwargs, node):
    """Handle [% b key1 key2 %] biblography reference shortcodes."""
    util.require((len(pargs) > 0) and (not kwargs), "Bad 'b' shortcode")

    used = util.make_config("bibliography")
    used.update(pargs)

    base = "@root/bibliography"
    links = [f'<a class="bib-ref" href="{base}/#{k}">{k}</a>' for k in pargs]
    links = ", ".join(links)
    return f'<span class="bib-ref">[{links}]</span>'


@shortcodes.register("bibliography")
def bibliography(pargs, kwargs, node):
    """Convert bibliography to HTML."""
    util.require((not pargs) and (not kwargs), "Bad 'bibliography' shortcode")
    if (filename := ivy.site.config.get("bibliography", None)) is None:
        return '<p class="warning">No bibliography specified.</p>'
    if (stylename := ivy.site.config.get("bibliography_style", None)) is None:
        util.fail("No bibliography style specified")

    bib = _read_bibliography(filename, stylename)

    html = find_plugin("pybtex.backends", "html")()

    def _format(key, body):
        return f'<dt id="{key}">{key}</dt>\n<dd>{body}</dd>'

    entries = [_format(entry.key, entry.text.render(html)) for entry in bib]
    return '<dl class="bib-list">\n\n' + "\n\n".join(entries) + "\n\n</dl>"


@ivy.events.register(ivy.events.Event.EXIT)
def check():
    """Check that bibliogrpahy entries are defined and used."""
    if (filename := ivy.site.config.get("bibliography", None)) is None:
        return
    if (stylename := ivy.site.config.get("bibliography_style", None)) is None:
        util.fail("No bibliography style specified")

    bib = _read_bibliography(filename, stylename)
    defined = {e.key for e in bib.entries}

    if (used := util.get_config("bibliography")) is None:
        return

    util.warn("unknown bibliography references", used - defined)
    util.warn("unused bibliography entries", defined - used)


def _read_bibliography(filename, style):
    """Load the bibliography file."""
    filename = Path(ivy.site.home(), filename)
    bib = parse_file(filename)

    style = find_plugin("pybtex.style.formatting", style)()
    return style.format_bibliography(bib)
