"""Record the date."""

from datetime import datetime

import ivy

@ivy.events.register(ivy.events.Event.INIT)
def build_date():
    """Add the date to the site configuration object."""
    ivy.site.config["build_date"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
