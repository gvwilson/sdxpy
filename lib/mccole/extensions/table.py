"""Handle tables.

In a better world, tables would be represented in Markdown as:

    | a | b |
    | - | - |
    | 1 | 2 |
    {: #slug caption="Some words"}

However, the Markdown parser doesn't accept attribute lists on tables,
so instead tables are represented as:

    <div class="table" id="slug" caption="Some words" markdown="1">
    | a | b |
    | - | - |
    | 1 | 2 |
    </div>

-   Each instance of the `Table` class stores information about a single table.

-   `table_ref` uses collected information to fill in table reference shortcodes
    of the form `[% t slug %]`.  It assumes there is a language defined by
    `config["lang"]` that matches a language in `util.TRANSLATIONS`

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

from dataclasses import dataclass

import ivy
import shortcodes
import util


@dataclass
class Table:
    """Keep track of information about a single table."""

    fileslug: str = ""
    slug: str = ""
    caption: str = ""
    number: tuple = ()


@shortcodes.register("t")
def table_ref(pargs, kwargs, node):
    """Handle [% t slug %] table reference."""
    if len(pargs) != 1:
        util.fail(f"Badly-formatted 't' shortcode {pargs} in {node.filepath}")

    if (tables := util.get_config("tables")) is None:
        return ""

    slug = pargs[0]
    if slug not in tables:
        util.fail(f"Unknown table cross-reference slug {slug} in {node.filepath}")
    table = tables[slug]
    label = util.make_label("table", table.number)
    return f'<a class="tbl-ref" href="@root/{table.fileslug}/#{slug}">{label}</a>'


@ivy.filters.register(ivy.filters.Filter.NODE_HTML)
def table_caption(text, node):
    """Get the caption in the right place."""

    def _replace(match):
        caption = match.group(1)
        cls = match.group(2)
        slug = match.group(4)
        table = util.get_config("tables")[slug]
        label = util.make_label("table", table.number)
        return f'<div class="{cls}"><table id="{slug}"><caption>{label}: {caption}</caption>'

    return util.TABLE_DIV.sub(_replace, text)


@ivy.events.register(ivy.events.Event.INIT)
def collect():
    """Collect table information using regular expressions."""
    tables = {}
    ivy.nodes.root().walk(lambda node: _process_tables(node, tables))
    _flatten_tables(tables)


def _process_tables(node, tables):
    """Collect table information."""
    tables[node.slug] = []
    for (i, match) in enumerate(util.TABLE.finditer(node.text)):
        if (caption := util.TABLE_CAPTION.search(match.group(0))) is None:
            util.fail(
                f"Table div '{match.group(0)}' without caption in {node.filepath}"
            )
        if (slug := util.TABLE_ID.search(match.group(0))) is None:
            util.fail(f"Table div '{match.group(0)}' without ID in {node.filepath}")
        tables[node.slug].append(
            Table(fileslug=node.slug, caption=caption.group(1), slug=slug.group(1))
        )


def _flatten_tables(collected):
    """Convert collected table information to flat lookup table."""
    major = util.make_major()
    tables = util.make_config("tables")
    for fileslug in collected:
        if fileslug in major:
            for (i, entry) in enumerate(collected[fileslug]):
                entry.number = (str(major[fileslug]), str(i + 1))
                tables[entry.slug] = entry
