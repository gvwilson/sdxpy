"""Handle FIXME markers."""

import shortcodes


@shortcodes.register("fixme")
def glossary_ref(pargs, kwargs, node):
    """Handle [% fixme ...args... %]."""
    return '<span class="FIXME">FIXME</span>'
