"""Handle FIXME markers."""

import shortcodes


@shortcodes.register("fixme")
def glossary_ref(pargs, kwargs, node):
    """Handle [% fixme ...args... %]."""
    pargs = " ".join(pargs)
    if pargs:
        pargs = f" {pargs}"
    kwargs = " ".join(f"{k}={v}" for k, v in kwargs.items())
    if kwargs:
        kwargs = f" {kwargs}"
    return f'<span class="fixme">FIXME{pargs}{kwargs}</span>'
