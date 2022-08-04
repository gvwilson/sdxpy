#!/usr/bin/env python

"""Check project."""


import argparse
import importlib.util
import re
from pathlib import Path

import utils
from bs4 import BeautifulSoup, Tag


CONFIGURATION = [
    ("abbrev", str),
    ("acknowledgments", str),
    ("acronym", str),
    ("appendices", list),
    ("author", str),
    ("bibliography", str),
    ("bibliography_style", str),
    ("chapters", list),
    ("copy", list),
    ("credits", str),
    ("debug", bool),
    ("exclude", list),
    ("extension", str),
    ("github", str),
    ("glossary", str),
    ("lang", str),
    ("links", str),
    ("markdown_settings", dict),
    ("out_dir", str),
    ("src_dir", str),
    ("tagline", str),
    ("theme", str),
    ("title", str),
    ("warnings", bool),
]
IGNORE_FILE = ".mccoleignore"
INDEX_FILE = "index.md"
RE_CODE_BLOCK = re.compile('```.+?```', re.DOTALL)
RE_CODE_INLINE = re.compile('`.+?`')
RE_FILE = re.compile(r'\[%\s*excerpt\b.+?f="(.+?)".+?%\]')
RE_FIGURE = re.compile(r'\[%\s*figure\b.+?img="(.+?)".+?%\]', re.DOTALL)
RE_LINK = re.compile(r'\[[^]]+?\]\[(\w+?)\]')
RE_PAT = re.compile(r'\[%\s*excerpt\b.+?pat="(.+?)"\s+fill="(.+?)".+?%\]')
RE_SHORTCODE = re.compile(r'\[%.+?%\]')


def main():
    """Main driver."""
    options = parse_args()

    check_config(options.config)

    source_files = get_src(options)
    check_files(source_files)
    check_links(options.links, source_files)

    html_files = get_html(options)
    check_dom(options.dom, html_files)


def check_config(config_path):
    """Check configuration file."""
    def _require(m, field, kind):
        if field not in dir(m):
            print(f"Configuration does not have {field}")
        elif not isinstance(getattr(m, field), kind):
            print(f"Configuration value for {field} is not {str(kind)}")

    spec = importlib.util.spec_from_file_location("config", config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for (field, kind) in CONFIGURATION:
        _require(module, field, kind)


def check_dom(dom_spec, html_files):
    """Check DOM elements in generated files."""
    allowed = utils.read_yaml(dom_spec)
    seen = {}
    for filename in html_files:
        with open(filename, "r") as reader:
            dom = BeautifulSoup(reader.read(), "html.parser")
            _collect_dom(seen, dom)
    _diff_dom(seen, allowed)


def check_files(source_files):
    """Check for excerpts and figures."""
    for (dirname, filename) in source_files:
        filepath = Path(dirname, filename)
        referenced = get_excerpts(filepath) | get_figures(filepath)
        existing = get_files(dirname) - get_ignores(dirname)
        report(f"{dirname}: excerpts", referenced, existing)


def check_links(links_file, source_files):
    """Check that all links are known."""
    existing = {entry["key"] for entry in utils.read_yaml(links_file)}
    referenced = set()
    for (dirname, filename) in source_files:
        referenced |= get_links(Path(dirname, filename))
    report("links", referenced, existing)


def get_excerpts(filename):
    """Find excerpt filenames."""
    with open(filename, "r") as reader:
        text = reader.read()
        result = {m.group(1) for m in RE_FILE.finditer(text)}
        pats = [(m.group(1), m.group(2)) for m in RE_PAT.finditer(text)]
        for (pat, fill) in pats:
            result |= {pat.replace("*", f) for f in fill.split()}
        return result


def get_files(dirname):
    """Return set of files."""
    return set(
        f.name
        for f in Path(dirname).iterdir()
        if f.is_file() and (f.name != INDEX_FILE)
    )


def get_figures(filepath):
    """Return all figures."""
    with open(filepath, "r") as reader:
        text = reader.read()
        return {m.group(1) for m in RE_FIGURE.finditer(text)}


def get_html(options):
    """Get paths to HTML files for processing."""
    return list(Path(options.html).glob("**/*.html"))


def get_ignores(dirname):
    """Get list of files in a directory that are intentionally unreferenced."""
    result = {IGNORE_FILE}
    ignore = Path(dirname, ".mccoleignore")
    if ignore.exists():
        with open(ignore, "r") as reader:
            result |= {x.strip() for x in reader.readlines()}
    return result


def get_links(filename):
    """Get Markdown [text][key] links from file."""
    with open(filename, "r") as reader:
        text = reader.read()
        text = RE_CODE_BLOCK.sub("", text)
        text = RE_CODE_INLINE.sub("", text)
        text = RE_SHORTCODE.sub("", text)
        return {m.group(1) for m in RE_LINK.finditer(text)}


def get_src(options):
    """Get (file, dir) pairs for processing."""
    result = [(options.src, INDEX_FILE)]
    subdirs = [s for s in Path(options.src).iterdir() if s.is_dir()]
    return result + [(s, INDEX_FILE) for s in subdirs]


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--dom", required=True, help="YAML spec of allowed DOM")
    parser.add_argument("--html", required=True, help="HTML directory")
    parser.add_argument("--links", required=True, help="YAML file of links")
    parser.add_argument("--src", required=True, help="Source directory")
    return parser.parse_args()


def report(title, expected, actual):
    """Report problems."""
    if expected == actual:
        return
    print(title)
    for (subtitle, items) in [
        ("missing", expected - actual),
        ("extra", actual - expected),
    ]:
        if not items:
            continue
        print(f"- {subtitle}")
        for i in sorted(items):
            print(f"  - {i}")


def _collect_dom(seen, node):
    """Collect DOM element attributes from given node and its descendents."""
    if not isinstance(node, Tag):
        return
    if _skip_dom(node):
        return
    if node.name not in seen:
        seen[node.name] = {}
    for (key, value) in node.attrs.items():
        if key not in seen[node.name]:
            seen[node.name][key] = set()
        if isinstance(value, str):
            seen[node.name][key].add(value)
        else:
            for v in value:
                seen[node.name][key].add(v)
    for child in node:
        _collect_dom(seen, child)


def _diff_dom(actual, expected):
    """Show difference between two DOM structures."""
    for name in sorted(actual):
        if name not in expected:
            print(f"{name} seen but not expected")
            continue
        for attr in sorted(actual[name]):
            if attr not in expected[name]:
                print(f"{name}.{attr} seen but not expected")
                continue
            if expected[name][attr] == "any":
                continue
            for value in sorted(actual[name][attr]):
                if value not in expected[name][attr]:
                    print(f"{name}.{attr} == '{value}' seen but not expected")


def _skip_dom(node):
    """Ignore this node and its children?"""
    return (
        (node.name == "div")
        and node.has_attr("class")
        and ("highlight" in node["class"])
    )


if __name__ == "__main__":
    main()
