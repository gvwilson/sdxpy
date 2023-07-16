"""Record the date."""

from datetime import datetime

import ark
import shortcodes
import util


@ark.events.register(ark.events.Event.INIT)
def build_date():
    """Add the date to the site configuration object."""
    ark.site.config["build_date"] = datetime.utcnow().strftime("%Y-%m-%d")


@shortcodes.register("date")
def thanks(pargs, kwargs, node):
    """Handle [% date %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'date' shortcode with {pargs} and {kwargs}",
    )
    return ark.site.config["build_date"]
