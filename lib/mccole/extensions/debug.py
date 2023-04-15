"""Print debugging information."""

import sys
import ivy
import shortcodes


@shortcodes.register("debug")
def debug(pargs, kwargs, node):
    """Insert credits."""
    print(f"NODE {node} class_list {node.get_class_list()} slug {node.get_slug_list()} template {node.get_template_list()} meta {node.meta} slug {node.slug} stem {node.stem}", file=sys.stderr)
    print(f"PARGS {pargs}", file=sys.stderr)
    print(f"KWARGS {kwargs}", file=sys.stderr)
