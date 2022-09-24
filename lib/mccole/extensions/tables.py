"""Handle tables.

In a better world, tables would be represented in Markdown as:

    | a | b |
    | - | - |
    | 1 | 2 |
    {: #slug caption="Some words"}

However, the Markdown parser doesn't accept attribute lists on tables,
so tables are represented as:

    <div class="table" id="slug" caption="Some words" markdown="1">
    | a | b |
    | - | - |
    | 1 | 2 |
    </div>

-   `Table` stores information about a single table.

-   `table_ref` uses collected information to fill in `[%t slug %]`
    shortcodes.

-   `table_caption` modifies the generated HTML to turn:

        <div class="table" id="slug" caption="Some words">
        <table>
        ...
        </table>
        </div>

    into:

        <div class="table">
        <table id="slug">
        <caption>Some words</caption>
        ...
        </table>
        </div>

-   `collect` scans Markdown files to find tables and number them.

"""

import ivy
import shortcodes
import util


@shortcodes.register("t")
def table_ref(pargs, kwargs, node):
    """Handle [%t slug %] table reference."""
    util.require(
        len(pargs) == 1, f"Badly-formatted 't' shortcode {pargs} in {node.filepath}"
    )

    # Too early in the processing cycle.
    if (tables := util.get_config("tables")) is None:
        return ""

    # Fill in.
    slug = pargs[0]
    util.require(
        slug in tables, f"Unknown table reference slug {slug} in {node.filepath}"
    )
    table = tables[slug]
    label = util.make_label("table", table.number)
    cls = 'class="tbl-ref"'
    return f'<a {cls} href="@root/{table.fileslug}/#{slug}">{label}</a>'


@ivy.filters.register(ivy.filters.Filter.NODE_HTML)
def table_caption(text, node):
    """Get the caption in the right place."""

    return util.TABLE_DIV.sub(_table_caption_replace, text)


def _table_caption_replace(match):
    caption = util.markdownify(match.group(1))
    cls = match.group(2).split()
    util.require(cls[0] == "table", f"Bad class(es) for table {cls}")
    slug = match.group(4)
    table = util.get_config("tables")[slug]
    label = util.make_label("table", table.number)
    cap = f"<caption>{label}: {caption}</caption>"
    tbl_cls = ' class="table-here"' if "table-here" in cls else ""
    result = f'<div class="table"><table id="{slug}"{tbl_cls}>{cap}'
    if "pagebreak" in cls:
        result = '<div class="pagebreak"></div>\n{result}'
    return result
