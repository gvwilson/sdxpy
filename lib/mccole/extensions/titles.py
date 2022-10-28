from dataclasses import dataclass

import ivy
import shortcodes
import util


@ivy.events.register(ivy.events.Event.INIT)
def collect():
    """Collect information from pages."""
    major = util.make_major()
    collected = {}
    ivy.nodes.root().walk(lambda node: _collect(node, major, collected))
    _cleanup(collected)


def _collect(node, major, collected):
    """Pull data from a single node."""
    if "title" in node.meta:
        collected[node.slug] = node.meta["title"]


def _cleanup(collected):
    chapters = [(slug, collected[slug]) for slug in ivy.site.config["chapters"]]
    appendices = [(slug, collected[slug]) for slug in ivy.site.config["appendices"]]
    util.make_config("titles", {"chapters": chapters, "appendices": appendices})
