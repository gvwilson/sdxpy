"""Handle raw images (not in figures)."""

from textwrap import dedent

import shortcodes
import util


@shortcodes.register("image")
@util.timing
def image(pargs, kwargs, node):
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
    relpath = ".." if util.is_slide_file(node) else "."
    src = f"{relpath}/{src}"
    width = "" if (width is None) else f' width="{width}"'

    return dedent(f"""<img src="{src}" alt="{alt}"{width}/>""")
