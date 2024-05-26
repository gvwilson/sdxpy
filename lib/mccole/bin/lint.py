"""Check project."""

import argparse
import ark
from bs4 import BeautifulSoup, NavigableString, Tag
from collections import Counter
import frontmatter
import importlib.util
from pathlib import Path
import re
import shortcodes
import yaml


# File types ignored when checking for inclusions
IGNORED_SUFFIXES = {
    ".bkp",
    ".md",
    ".pdf",
    ".png",
    ".svg",
    ".tbl"
}

# Shortcode keys that are required to be unique
UNIQUE_KEYS = {
    "fig_def",
    "gloss",
    "tbl_def",
}


@ark.filters.register(ark.filters.Filter.LOAD_NODE_FILE)
def keep_file(value, path):
    """Only process .md Markdown files."""
    return path.suffix == ".md"


def main():
    options = parse_args()
    options.config = load_config(options)
    options.html = find_html_files(options)

    check_html(options)

    links = check_redundant_links(options)
    check_colophon(options, links)

    found, metadata = collect_all()
    check_metadata(metadata)
    for func in [
        check_bib,
        check_fig,
        check_inc,
        check_tbl,
        check_xref,
    ]:
        func(options, found)

    gloss_internal_keys = check_gloss_internal(options)
    check_gloss(options, found, gloss_internal_keys)


def check_bib(options, found):
    """Check bibliography citations."""
    expected = get_bib_keys(options)
    compare_keys("bibliography", expected, found["bib"])


def check_colophon(options, actual):
    """Check all colophon links are present."""
    actual_keys = set([e["key"] for e in actual])
    expected = yaml.safe_load(Path(options.root, "lib", "mccole", "colophon.yml").read_text())
    expected_keys = set([e["key"] for e in expected])
    missing = expected_keys - actual_keys
    if missing:
        print(f"Missing colophon link(s): {listify(missing)}")


def check_fig(options, found):
    """Check figure definitions and citations."""
    compare_keys("figure", set(found["fig_def"].keys()), found["fig_ref"])


def check_gloss(options, found, internal):
    """Check glossary citations."""
    expected = get_gloss_keys(options)
    compare_keys("gloss", expected, found["gloss"], extra=internal)


def check_gloss_internal(options):
    """Check internal references in glossary."""
    text = Path(options.root, "info", "glossary.yml").read_text()

    glossary = yaml.safe_load(text) or []
    actual = Counter([e["key"] for e in glossary])
    duplicates = {k for k, v in actual.items() if v > 1}
    if duplicates:
        print(f"duplicate glossary key(s) {listify(duplicates)}")

    internal = set(re.findall(r'\[.+?\]\(#(.+?)\)', text, re.DOTALL))
    for entry in glossary:
        if "ref" in entry:
            internal.update(set(entry["ref"]))

    unknown = internal - {e["key"] for e in glossary}
    if unknown:
        print(f"unknown internal glossary key(s) {listify(unknown)}")

    return internal


def check_html(options):
    """Check generated HTML pages."""
    for filename in options.html:
        with open(filename, "r") as reader:
            dom = BeautifulSoup(reader.read(), "html.parser")
            visit_html(filename, dom)


def check_inc(options, found):
    """Check file inclusions."""
    expected = get_includable_files(options)
    compare_keys("inc", expected, found["inc"])


def check_metadata(metadata):
    """Check index and slides metadata."""
    index_keys = set(metadata["index"].keys())
    slides_keys = set(metadata["slides"].keys())
    unmatched = index_keys.symmetric_difference(slides_keys)
    if unmatched:
        print(f"unmatched index/slides slugs: {', '.join(sorted(unmatched))}")
    matched = index_keys.intersection(slides_keys)
    errors = {key for key in matched if metadata["index"][key] != metadata["slides"][key]}
    if errors:
        print(f"mis-matched title(s): {', '.join(errors)}")


def check_redundant_links(options):
    """Look for redundant link definitions."""
    links = yaml.safe_load(Path(options.root, "info", "links.yml").read_text()) or []
    count = Counter(entry["url"] for entry in links)
    problems = [url for url in count if count[url] > 1]
    if problems:
        print(f"redundant link definitions: {', '.join(sorted(problems))}")
    return links


def check_tbl(options, found):
    """Check table definitions and citations."""
    compare_keys("table", set(found["tbl_def"].keys()), found["tbl_ref"])


def check_xref(options, found):
    """Check chapter/appendix cross-references."""
    expected = options.config.chapters + options.config.appendices
    compare_keys("cross-ref", expected, found["xref"], unused=False)


def collect_all():
    """Collect values from Markdown files."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(collect_bib, "b")
    parser.register(collect_fig_def, "figure")
    parser.register(collect_fig_ref, "f")
    parser.register(collect_gloss, "g")
    parser.register(collect_inc, "inc")
    parser.register(collect_tbl_def, "table")
    parser.register(collect_tbl_ref, "t")
    parser.register(collect_xref, "x")
    collected = {
        "bib": {},
        "fig_def": {},
        "fig_ref": {},
        "gloss": {},
        "inc": {},
        "tbl_def": {},
        "tbl_ref": {},
        "xref": {},
    }
    metadata = {
        "index": {},
        "slides": {},
    }
    ark.nodes.root().walk(
        lambda node: collect_visitor(node, parser, collected, metadata)
    )
    return collected, metadata


def collect_bib(pargs, kwargs, found):
    """Collect data from a bibliography reference shortcode."""
    found["bib"].update(pargs)


def collect_fig_def(pargs, kwargs, found):
    """Collect data from a figure definition shortcode."""
    slug = kwargs["slug"]
    if slug in found["fig_def"]:
        print(f"Duplicate definition of figure slug {slug}")
    else:
        found["fig_def"].add(slug)


def collect_fig_ref(pargs, kwargs, found):
    """Collect data from a figure reference shortcode."""
    found["fig_ref"].add(pargs[0])


def collect_gloss(pargs, kwargs, found):
    """Collect data from a glossary reference shortcode."""
    found["gloss"].add(pargs[0])


def collect_inc(pargs, kwargs, found):
    """Collect data from an inclusion shortcode."""
    found["inc"].add(f"{found['_dirname_']}/{pargs[0]}")


def collect_tbl_def(pargs, kwargs, found):
    """Collect data from a table definition shortcode."""
    slug = kwargs.get("slug", None) or str(Path(kwargs["tbl"]).stem)
    if slug in found["tbl_def"]:
        print("Duplicate definition of table slug {slug}")
    else:
        found["tbl_def"].add(slug)


def collect_tbl_ref(pargs, kwargs, found):
    """Collect data from a table reference shortcode."""
    found["tbl_ref"].add(pargs[0])


def collect_title(node, metadata):
    if not node.path:
        return
    front = frontmatter.loads(node.text)
    title = front.get("title", None)
    if len(node.path) == 1:
        metadata["index"][node.slug] = front["title"]
    elif (len(node.path) == 2) and node.slug == "slides":
        metadata["slides"][node.parent.slug] = front["title"]


def collect_xref(pargs, kwargs, found):
    """Collect data from a cross-reference shortcode."""
    found["xref"].add(pargs[0])


def collect_visitor(node, parser, collected, metadata):
    """Visit each node, collecting data."""
    collect_title(node, metadata)
    if Path(node.filepath).name != "index.md":
        return
    found = {key: set() for key in collected.keys()}
    found["_dirname_"] = f"src/{node.slug}"
    parser.parse(node.text, found)
    for kind in found:
        if kind != "_dirname_":
            reorganize_found(node, kind, collected, found)


def compare_keys(kind, expected, actual, extra=None, unused=True):
    """Check two sets of keys."""
    for key, slugs in actual.items():
        if key not in expected:
            print(f"unknown {kind} {key} used in {listify(slugs)}")
        else:
            expected.remove(key)
    if extra:
        expected -= extra
    if unused and expected:
        print(f"unused {kind} {listify(expected)}")


def find_html_files(options):
    """Get list of all generated HTML files."""
    candidates = Path(options.htmldir).rglob("**/*.html")
    if options.skipslides:
        candidates = (x for x in candidates if '/slides/' not in str(x))
    return list(candidates)


def get_bib_keys(options):
    """Get actual bibliography keys."""
    text = Path(options.root, "info", "bibliography.bib").read_text()
    return set(re.findall(r"^@.+?\{(.+?),$", text, re.MULTILINE))


def get_gloss_keys(options):
    """Get actual glossary keys."""
    text = Path(options.root, "info", "glossary.yml").read_text()
    glossary = yaml.safe_load(text) or []
    if isinstance(glossary, dict):
        glossary = [glossary]
    return {entry["key"] for entry in glossary}


def get_includable_files(options):
    """Get all includable files from source directory."""
    result = set()
    for slug in options.config.chapters + options.config.appendices:
        for filename in Path(options.root, "src", slug).rglob("**/*"):
            if is_includable(options, filename):
                result.add(str(filename))
    return result


def is_includable(options, filename):
    """Might this thing be included?"""
    if filename.is_dir():
        return False
    if filename.suffix in IGNORED_SUFFIXES:
        return False
    if filename.name in options.exclude:
        return False
    filestr = str(filename)
    if filestr.endswith("~"):
        return False
    if filestr in options.config.unincluded:
        return False
    return True


def listify(values):
    """Format values for printing."""
    return ", ".join(sorted(list(values)))


def load_config(options):
    """Load configuration file as module."""
    filename = Path(options.root, "config.py")
    spec = importlib.util.spec_from_file_location("config", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dom", required=True, help="DOM specification file")
    parser.add_argument("--exclude", nargs="+", help="Includable files to ignore")
    parser.add_argument("--htmldir", required=True, help="HTML directory")
    parser.add_argument("--root", required=True, help="Root directory")
    parser.add_argument(
        "--skipslides",
        action="store_true",
        default=False,
        help="skip slides when checking HTML"
    )
    options = parser.parse_args()
    options.exclude = set(options.exclude)
    return options


def reorganize_found(node, kind, collected, found):
    """Copy found keys into overall collection."""
    for key in found[kind]:
        if key not in collected[kind]:
            collected[kind][key] = set()
        elif kind in UNIQUE_KEYS:
            print(f"{kind} key {key} redefined")
        slug = node.slug if node.slug else "@root"
        collected[kind][key].add(slug)


def visit_html(filename, node):
    """Recursively check nodes of DOM tree."""
    if isinstance(node, NavigableString):
        if "][" in node.text:
            print(f"{filename} dangling ][: '''{node.text}'''")
    elif not isinstance(node, Tag):
        return
    elif node.name in {"code", "pre"}:
        return
    for child in node:
        visit_html(filename, child)


if __name__ == "__main__":
    main()
