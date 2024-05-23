"""Initialization required by template."""

import ark
from datetime import datetime
from pathlib import Path
import re
import shortcodes
from shutil import copyfile
import util

WHITESPACE = re.compile(r'\s+')


@ark.events.register(ark.events.Event.INIT_BUILD)
@util.timing
def init_build():
    """Launch startup tasks in order."""
    _init_date()
    _init_contents()
    _collect_metadata()
    _decorate_metadata()
    _collect_shortcodes()
    _append_links()


@ark.events.register(ark.events.Event.EXIT_BUILD)
def exit_build():
    """Run finalization tasks in order."""
    _copy_files()
    _report_timing()


def _append_links():
    """Add links to node text."""
    util.ensure_links()
    links_block = ark.site.config["_links_block_"]

    def _visitor(node):
        if (node.ext == "md"):
            node.text += "\n\n" + links_block

    ark.nodes.root().walk(_visitor)


def _collect_metadata():
    """Collect all metadata from nodes."""
    metadata = {}

    def _visitor(node):
        if util.is_index_file(node):
            slug = node.slug if node.slug else "@root"
            metadata[slug] = node.meta

    ark.nodes.root().walk(_visitor)
    ark.site.config["_meta_"] = metadata


def _collect_shortcodes():
    """Collect information from shortcodes."""

    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_collect_shortcodes_figures, "figure")
    parser.register(_collect_shortcodes_glossary, "g")
    parser.register(_collect_shortcodes_index, "i")
    parser.register(_collect_shortcodes_tables, "table")

    collector = {}
    ark.nodes.root().walk(
        lambda node: _collect_shortcodes_visitor(node, parser, collector)
    )

    ark.site.config["_figures_"] = {}
    ark.site.config["_index_"] = {}
    ark.site.config["_tables_"] = {}
    ark.site.config["_terms_"] = {}
    for slug, seen in collector.items():
        ark.site.config["_index_"][slug] = set(seen["index"])
        ark.site.config["_terms_"][slug] = set(seen["terms"])
        for key, number in seen["figures"].items():
            ark.site.config["_figures_"][key] = number
        for key, number in seen["tables"].items():
            ark.site.config["_tables_"][key] = number


def _collect_shortcodes_figures(pargs, kwargs, extra):
    """Collect data from a figure shortcode."""
    util.require(
        "slug" in kwargs,
        f"Bad 'figure' in {extra['filename']}: '{pargs}' and '{kwargs}'",
    )
    extra["figures"].append(kwargs["slug"])


def _collect_shortcodes_glossary(pargs, kwargs, extra):
    """Collect data from a glossary reference shortcode."""
    util.require(
        len(pargs) == 2,
        f"Bad 'g' in {extra['filename']}: '{pargs}' and '{kwargs}'",
    )
    extra["terms"].append(pargs[0])


def _collect_shortcodes_index(pargs, kwargs, extra):
    """Collect data from an index reference shortcode."""
    for term in pargs:
        extra["index"].append(WHITESPACE.sub(' ', term).strip())


def _collect_shortcodes_tables(pargs, kwargs, extra):
    """Collect data from a table shortcode."""
    util.require(
        "slug" in kwargs,
        f"Bad 'table' in {extra['filename']}: '{pargs}' and '{kwargs}'",
    )
    extra["tables"].append(kwargs["slug"])


def _collect_shortcodes_visitor(node, parser, collector):
    """Visit each node, collecting data."""
    if (not node.slug) or (not util.is_index_file(node)):
        return

    util.require(
        node.slug in ark.site.config["_meta_"],
        f"No metadata for {node.slug}",
    )
    util.require(
        "number" in ark.site.config["_meta_"][node.slug],
        f"No number in metadata for {node.slug}",
    )

    found = {
        "filename": node.filepath,
        "figures": [],
        "index": [],
        "tables": [],
        "terms": [],
    }
    parser.parse(node.text, found)
    number = ark.site.config["_meta_"][node.slug]["number"]
    collector[node.slug] = {
        "figures": {
            fig_slug: {"slug": f"{number}.{i + 1}", "node": node.slug}
            for i, fig_slug in enumerate(found["figures"])
        },
        "index": found["index"],
        "tables": {
            tbl_slug: {"slug": f"{number}.{i + 1}", "node": node.slug}
            for i, tbl_slug in enumerate(found["tables"])
        },
        "terms": found["terms"],
    }


def _copy_files():
    """Copy files from source directories (not recursive)."""
    for pat in ark.site.config["copy"]:
        src_dir = ark.site.src()
        out_dir = ark.site.out()
        for src_file in Path(src_dir).rglob(f"**/{pat}"):
            out_file = str(src_file).replace(src_dir, out_dir)
            Path(out_file).parent.mkdir(exist_ok=True, parents=True)
            copyfile(src_file, out_file)


def _decorate_metadata():
    """Number chapters and appendices."""
    metadata = ark.site.config["_meta_"]

    for i, slug in enumerate(ark.site.config["chapters"]):
        metadata[slug]["kind"] = util.kind("chapter")
        metadata[slug]["number"] = str(i + 1)

    for i, slug in enumerate(ark.site.config["appendices"]):
        metadata[slug]["kind"] = util.kind("appendix")
        metadata[slug]["number"] = chr(ord("A") + i)


def _init_contents():
    """Construct integrated list of chapters and appendices."""
    ark.site.config["_contents_"] = ark.site.config["chapters"] + ark.site.config["appendices"]


def _init_date():
    """Add the date to the site configuration object."""
    ark.site.config["_timestamp_"] = datetime.utcnow()


def _report_timing():
    """Print report of timing."""
    if not ark.site.config.get("timing", False):
        return
    timings = ark.site.config.get(util.TIMING, {})
    pairs = [(t, n) for (n, t) in timings.items()]
    pairs.sort(reverse=True)
    for (t, n) in pairs:
        print(f"{t:.2f}: {n}")
