"""Handle configuration values."""

import ark
import shortcodes
import util


@shortcodes.register("config")
@util.timing
def config(pargs, kwargs, node):
    """Handle [% config "key" %] shortcode."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 'config' shortcode in {node.path} with '{pargs}' and '{kwargs}'",
    )
    current = ark.site.config
    for key in pargs[0].split("."):
        try:
            current = current[key]
        except KeyError:
            util.fail(f"Bad config key '{pargs[0]}': no component '{key}'")
    return current
