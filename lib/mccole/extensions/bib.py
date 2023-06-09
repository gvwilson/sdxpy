"""Generate bibliography."""

from pathlib import Path

import ark
import shortcodes
import util
from pybtex.database import parse_file
from pybtex.plugin import find_plugin


@shortcodes.register("b")
def bibliography_ref(pargs, kwargs, node):
    """Handle [%b key1 key2 %] biblography reference shortcodes."""
    util.require(
        (len(pargs) > 0) and (not kwargs),
        f"Bad 'b' shortcode with {pargs} and {kwargs}",
    )

    used = util.make_config("bibliography")
    used.update(pargs)

    base = "@root/bibliography"
    links = [f'<a class="bib-ref" href="{base}/#{k}">{k}</a>' for k in pargs]
    links = ", ".join(links)
    return f'<span class="bib-ref">[{links}]</span>'


@shortcodes.register("bibliography")
def bibliography(pargs, kwargs, node):
    """Convert bibliography to HTML."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'bibliography' shortcode {pargs} and {kwargs}",
    )

    filename = ark.site.config.get("bibliography", None)
    util.require(filename is not None, "No bibliography specified")

    stylename = ark.site.config.get("bibliography_style", None)
    util.require(stylename is not None, "No bibliography style specified")

    bib = _read_bibliography(filename, stylename)
    html = find_plugin("pybtex.backends", "html")()

    def _format(key, body):
        return f'<dt id="{key}">{key}</dt>\n<dd>{body}</dd>'

    entries = [_format(entry.key, entry.text.render(html)) for entry in bib]
    return '<dl class="bib-list">\n\n' + "\n\n".join(entries) + "\n\n</dl>"


@ark.events.register(ark.events.Event.EXIT)
def check_bibliography():
    """Check that bibliogrpahy entries are defined and used."""
    if (filename := ark.site.config.get("bibliography", None)) is None:
        return
    if (stylename := ark.site.config.get("bibliography_style", None)) is None:
        return
    if (used := util.get_config("bibliography")) is None:
        return

    bib = _read_bibliography(filename, stylename)
    defined = {e.key for e in bib.entries}

    util.warn("unknown bibliography references", used - defined)
    util.warn("unused bibliography entries", defined - used)


def _read_bibliography(filename, style):
    """Load the bibliography file."""
    filename = Path(ark.site.home(), filename)
    bib = parse_file(filename)

    style = find_plugin("pybtex.style.formatting", style)()
    return style.format_bibliography(bib)
