import ibis
import ivy
import util


@ivy.events.register(ivy.events.Event.INIT)
def collect_titles():
    """Collect page titles."""
    info = {}
    ivy.nodes.root().walk(lambda node: _collect(info, node))
    chapters = [(slug, info[slug]) for slug in ivy.site.config["chapters"]]
    appendices = [(slug, info[slug]) for slug in ivy.site.config["appendices"]]
    util.make_config("titles", {"chapters": chapters, "appendices": appendices})


@ibis.filters.register("part_name")
def part_name(slug):
    """Insert chapter/appendix part name."""
    titles = util.get_config("titles")

    for (i, (s, title)) in enumerate(titles["chapters"]):
        if slug == s:
            label = (str(i+1),)
            return f'{util.make_label("part", label)}'

    for (i, (s, title)) in enumerate(titles["appendices"]):
        if slug == s:
            label = (chr(ord("A") + i),)
            return f'{util.make_label("part", label)}'

    fail(f"Unknown slug {slug}")


def _collect(info, node):
    if "title" in node.meta:
        info[node.slug] = node.meta["title"]
