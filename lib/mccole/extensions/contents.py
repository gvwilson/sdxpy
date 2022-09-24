import ibis
import util


@ibis.filters.register("part_name")
def part_name(slug):
    """Insert chapter/appendix part name."""
    titles = util.get_config("titles")

    for (i, (s, title)) in enumerate(titles["chapters"]):
        if slug == s:
            label = (str(i + 1),)
            return f'{util.make_label("part", label)}'

    for (i, (s, title)) in enumerate(titles["appendices"]):
        if slug == s:
            label = (chr(ord("A") + i),)
            return f'{util.make_label("part", label)}'

    util.fail(f"Unknown slug {slug}")
