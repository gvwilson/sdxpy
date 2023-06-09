"""Record the date."""

from datetime import datetime

import ark


@ark.events.register(ark.events.Event.INIT)
def build_date():
    """Add the date to the site configuration object."""
    ark.site.config["build_date"] = datetime.utcnow().strftime("%Y-%m-%d")
