"""Handle raw images (not in figures)."""

from textwrap import dedent

import ark
import shortcodes
import util


@shortcodes.register("image")
def figure_def(pargs, kwargs, node):
    """Handle image."""
    allowed = {"src", "alt", "width"}
    util.require(
        (not pargs) and allowed.issuperset(kwargs.keys()),
        f"Bad 'image' shortcode {pargs} and {kwargs} in {node}",
    )
    src = kwargs["src"]
    alt = util.markdownify(kwargs["alt"])
    width = kwargs.get("width", None)

    util.require_file(node, src, "image")
    src = f"../{src}" if util.is_slides(node) else src
    width = "" if (width is None) else f' width="{width}"'

    return dedent(
        f"""<img src="{src}" alt="{alt}"{width}/>"""
    )
