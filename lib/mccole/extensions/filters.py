"""Page elements."""

import ark
import ibis

import util


@ibis.filters.register("is_chapter")
@util.timing
def is_chapter(node):
    """Is this a chapter node (vs. appendix)?"""
    return node.slug and node.slug in ark.site.config["chapters"]


@ibis.filters.register("nav_next")
@util.timing
def nav_next(node):
    """Create next-page link."""
    return _nav_link(node, "next")


@ibis.filters.register("nav_prev")
@util.timing
def nav_prev(node):
    """Create previous-page link."""
    return _nav_link(node, "prev")


@ibis.filters.register("toc")
@util.timing
def toc(node):
    """Create table of contents."""
    chapters = util.chapter_list(node)
    chapters = f'<ol class="toc-chapters">{"".join(chapters)}</ol>'
    appendices = util.appendix_list(node)
    appendices = f'<ol class="toc-appendices">{"".join(appendices)}</ol>'
    return f'{chapters}\n{appendices}'


def _nav_link(node, kind):
    """Generate previous/next page links."""
    if not node.slug:
        return ""
    contents = ark.site.config["_contents_"]
    try:
        where = contents.index(node.slug)
    except ValueError:
        util.fail(f"unknown slug {node.slug} in {node.path}")
    if kind == "prev":
        if where == 0:
            return ""
        return f"@root/{contents[where - 1]}/"
    elif kind == "next":
        if where == (len(contents) - 1):
            return ""
        return f"@root/{contents[where + 1]}/"
    else:
        util.fail(f"Unknown nav link type '{kind}' in {node.path}")
