"""Headings and cross-references."""

import sys

import shortcodes
import util


@shortcodes.register("x")
def heading_ref(pargs, kwargs, node):
    """Handle [%x slug %] section reference."""
    util.require(
        (len(pargs) == 1) and not kwargs, f"Bad 'x' shortcode {pargs} and {kwargs}"
    )
    headings = util.get_config("headings")
    slug = pargs[0]
    try:
        heading = headings[slug]
        label = util.make_label("part", heading.number)
        anchor = f"#{slug}" if (len(heading.number) > 1) else ""
        cls = 'class="x-ref"'
        return f'<a {cls} href="@root/{heading.fileslug}/{anchor}">{label}</a>'
    except KeyError:
        print(f"Unknown part cross-reference key {slug}", file=sys.stderr)
        return "FIXME"
