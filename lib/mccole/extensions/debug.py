"""Print debugging information."""

import sys

import shortcodes


@shortcodes.register("debug")
def debug(pargs, kwargs, node):
    """Display debugging information."""
    print(
        f"NODE {node}"
        f" class_list {node.get_class_list()}"
        f" slug {node.get_slug_list()}"
        f" template {node.get_template_list()}"
        f" meta {node.meta}"
        f" slug {node.slug}"
        f" stem {node.stem}",
        file=sys.stderr,
    )
    print(f"PARGS {pargs}", file=sys.stderr)
    print(f"KWARGS {kwargs}", file=sys.stderr)
