"""Generate credits."""

import ivy
import shortcodes
import util
import yaml


@shortcodes.register("credits")
def bibliography(pargs, kwargs, node):
    """Insert credits."""
    util.require((not pargs) and (not kwargs), "Bad 'credits' shortcode")

    filename = ivy.site.config.get("credits", None)
    util.require(filename is not None, "No credits specified")

    lang = ivy.site.config.get("lang", None)
    util.require(lang is not None, "No language specified")

    with open(filename, "r") as reader:
        credits = yaml.safe_load(reader)
    return "\n\n".join([e[lang] for e in credits])
