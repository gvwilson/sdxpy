"""Filters for use in template expansion."""

import ibis
import util


@ibis.filters.register("is_root")
def is_root(node):
    """Is this the root node?"""
    return len(node.path) == 0


@ibis.filters.register("not_root")
def not_root(node):
    """Is this _not_ the root node?"""
    return not is_root(node)


@ibis.filters.register("part_name")
def part_name(node):
    """Insert chapter/appendix part name."""
    headings = util.get_config("headings")
    util.require(node.slug in headings, f"Unknown slug for part name {node.slug}")
    entry = headings[node.slug]
    return f'{util.make_label("part", entry.number)}'


@ibis.filters.register("part_title")
def part_title(node):
    """Insert chapter/appendix title."""
    return util.get_title(node)
