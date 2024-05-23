"""Ark shortcodes."""

from pathlib import Path
import ark
import shortcodes

import util


@shortcodes.register("b")
@util.timing
def bibliography_ref(pargs, kwargs, node):
    """Handle [%b key1 key2 %] biblography references."""
    util.require(
        (len(pargs) > 0) and (not kwargs),
        f"Bad 'b' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    base = "@root/bib"
    links = [f'<a class="bib-ref" href="{base}/#{k}">{k}</a>' for k in pargs]
    links = ", ".join(links)
    return f'<span class="bib-ref">[{links}]</span>'


@shortcodes.register("bibliography")
@util.timing
def bibliography(pargs, kwargs, node):
    """Handle [% bibliography %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'bibliography' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    return Path(ark.site.home(), "tmp", "bibliography.html").read_text()
