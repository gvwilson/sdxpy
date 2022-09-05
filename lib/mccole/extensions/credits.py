"""Generate credits."""

import ivy
import shortcodes
import yaml

import util


@shortcodes.register("credits")
def bibliography(pargs, kwargs, node):
    """Insert credits."""
    util.require((not pargs) and (not kwargs), "Bad 'credits' shortcode")
    if (filename := ivy.site.config.get("credits", None)) is None:
        return '<p class="warning">No credits specified.</p>'
    with open(filename, "r") as reader:
        credits = yaml.safe_load(reader)
    return "\n\n".join([e["bio"] for e in credits])
