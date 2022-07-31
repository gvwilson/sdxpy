import ivy
import util


@ivy.events.register(ivy.events.Event.INIT)
def collect_titles():
    """Collect page titles."""
    info = {}
    ivy.nodes.root().walk(lambda node: _collect(info, node))
    chapters = [(slug, info[slug]) for slug in ivy.site.config["chapters"]]
    appendices = [(slug, info[slug]) for slug in ivy.site.config["appendices"]]
    config = util.mccole()
    config["titles"] = {"chapters": chapters, "appendices": appendices}


def _collect(info, node):
    if "title" in node.meta:
        info[node.slug] = node.meta["title"]
