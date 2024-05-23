"""Handle table references and tables."""

import ark
from pathlib import Path
import shortcodes

import util


@shortcodes.register("t")
@util.timing
def table_ref(pargs, kwargs, node):
    """Handle [%t slug %] table reference shortcode."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 't' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    slug = pargs[0]
    known = ark.site.config["_tables_"]
    util.require(slug in known, f"Unknown table slug {slug} in {node.path}")
    number = known[slug]["slug"]
    file_slug = known[slug]["node"]
    caption = f"{util.kind('table')}&nbsp;{number}"
    return f'<a class="tbl-ref" href="@root/{file_slug}/#{slug}">{caption}</a>'


@shortcodes.register("table")
@util.timing
def table_def(pargs, kwargs, node):
    """Handle table definition."""
    allowed = {"slug", "tbl", "caption"}
    util.require(
        (not pargs) and util.allowed(kwargs, allowed),
        f"Bad 'table' in {node.path}: '{pargs}' and '{kwargs}'",
    )

    slug = util.get_table_slug(kwargs, node.path)
    tbl = kwargs["tbl"]
    caption = util.markdownify(kwargs["caption"])

    util.require_file(node, tbl, "table")
    known = ark.site.config["_tables_"]
    if util.is_index_file(node):
        label = f"{util.kind('table')}&nbsp;{known[slug]['slug']}: "
    elif util.is_slide_file(node):
        label = ""
    else:
        util.fail(f"Unknown node type for table {node}")
    content = util.markdownify(Path(Path(node.filepath).parent, tbl).read_text())
    content = content.replace("<table>", f'<table id="{slug}"><caption>{label}{caption}</caption>')
    return content
