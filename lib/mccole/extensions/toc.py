"""Table of contents and related cross-references."""

import ark
import shortcodes

import util


@shortcodes.register("toc")
@util.timing
def table_of_contents(pargs, kwargs, node):
    """Handle [% toc %] table of contents shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'toc' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    chapters = util.chapter_list(node)
    chapters = f'<div class="col-6"><ol class="toc-chapters">{"".join(chapters)}</ol></div>'
    appendices = util.appendix_list(node)
    appendices = f'<div class="col-6"><ol class="toc-appendices">{"".join(appendices)}</ol></div>'
    return f'<div class="row">{chapters}\n{appendices}</div>'


@shortcodes.register("x")
@util.timing
def cross_ref(pargs, kwargs, node):
    """Handle [%x slug %] cross-reference shortcode."""
    util.require(
        (len(pargs) == 1) and util.allowed(kwargs, {"kind"}),
        f"Bad 'x' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    slug = pargs[0]
    util.require(
        slug in ark.site.config["_meta_"],
        f"Unknown cross-reference key '{slug}' in {node.path}",
    )
    kind = kwargs.get("kind", None)
    return util.cross_ref(slug, kind)
