#!/usr/bin/env python

"""Check project."""


import argparse
import re
from fnmatch import fnmatch
from pathlib import Path

import utils
from bs4 import BeautifulSoup, Tag
import yaml
from yaml_header_tools import NoValidHeader, get_header_from_file


DIRECTIVES_FILE = ".mccole"

CONFIGURATION = [
    ("abbrev", str),
    ("acknowledgments", str),
    ("acronym", str),
    ("appendices", dict),
    ("author", str),
    ("bibliography", str),
    ("bibliography_style", str),
    ("chapters", dict),
    ("copy", list),
    ("credits", str),
    ("debug", bool),
    ("exclude", list),
    ("extension", str),
    ("glossary", str),
    ("lang", str),
    ("links", str),
    ("markdown_settings", dict),
    ("out_dir", str),
    ("repo", str),
    ("src_dir", str),
    ("tagline", str),
    ("theme", str),
    ("title", str),
    ("warnings", bool),
]
INDEX_FILE = "index.md"
MAKEFILE = "Makefile"
RE_CODE_BLOCK = re.compile("```.+?```", re.DOTALL)
RE_CODE_INLINE = re.compile("`.+?`")
RE_FILE = re.compile(r'\[%\s*inc\b.+?(file|html)="(.+?)".+?%\]')
RE_FIGURE = re.compile(r'\[%\s*figure\b.+?img="(.+?)".+?%\]', re.DOTALL)
RE_LINK = re.compile(r"\[[^]]*?\]\[(\w+?)\]")
RE_PAT = re.compile(r'\[%\s*inc\b.+?pat="(.+?)"\s+fill="(.+?)".+?%\]')
RE_SHORTCODE = re.compile(r"\[%.+?%\]")
SLIDES_FILE = "slides.html"
SLIDES_TEMPLATE = "slides"

EXPECTED_FILES = {DIRECTIVES_FILE, INDEX_FILE, MAKEFILE, SLIDES_FILE}


def main():
    """Main driver."""
    options = parse_args()

    config = check_config(options.config)
    glossary_file = getattr(config, "glossary")
    language = getattr(config, "lang")
    links_file = getattr(config, "links")
    out_dir = getattr(config, "out_dir")
    src_dir = getattr(config, "src_dir")
    unreferenced = set(getattr(config, "unreferenced", []))

    source_files = get_src(src_dir)
    check_files(src_dir, source_files, unreferenced)
    check_glossary(glossary_file, language)
    check_links(links_file, source_files)
    check_slides(source_files)

    html_files = get_html(out_dir)
    check_dom(options.dom, html_files)


def check_config(config_path):
    """Check configuration file."""

    def _require(m, field, kind):
        if field not in dir(m):
            print(f"Configuration does not have {field}")
        elif not isinstance(getattr(m, field), kind):
            print(f"Configuration value for {field} is not {str(kind)}")

    module = utils.load_config(config_path)
    for (field, kind) in CONFIGURATION:
        _require(module, field, kind)

    return module


def check_dom(dom_spec, html_files):
    """Check DOM elements in generated files."""
    allowed = utils.read_yaml(dom_spec)
    seen = {}
    for filename in html_files:
        text = _read_html(filename)
        dom = BeautifulSoup(text, "html.parser")
        _collect_dom(seen, dom)
    _diff_dom(seen, allowed)


def check_files(source_dir, source_files, unreferenced):
    """Check for inclusions and figures."""
    for (dirname, filename) in source_files:
        filepath = Path(dirname, filename)
        referenced = get_inclusions(filepath) | get_figures(filepath)
        existing = get_files(source_dir, dirname, unreferenced)
        report(f"{dirname}: inclusions", referenced, existing)


def check_glossary(glossary_file, language):
    """Check internal consistency of glossary."""
    glossary = utils.read_yaml(glossary_file)
    missing_keys = [g for g in glossary if "key" not in g]
    if missing_keys:
        print(f"glossary entries without keys: {missing_keys}")
        return

    glossary = {g["key"]: g for g in glossary}
    for (key, entry) in sorted(glossary.items()):
        if language not in entry:
            print(f"glossary entry {key} missing {language}")
        elif "ref" in entry and any(r not in glossary for r in entry["ref"]):
            print(f"missing ref(s) in glossary entry {key}")
        elif "def" not in entry[language]:
            print(f"glossary entry {key}/{language} missing 'def'")


def check_links(links_file, source_files):
    """Check that all links are known."""
    existing = {
        entry["key"]
        for entry in utils.read_yaml(links_file)
        if not entry.get("direct", False)
    }
    referenced = set()
    for (dirname, filename) in source_files:
        referenced |= get_links(Path(dirname, filename))
    report("links", referenced, existing)


def check_slides(source_files):
    """Check slides.html files if they exist."""
    for (dir_path, index_file) in source_files:
        slides_path = Path(dir_path, SLIDES_FILE)
        if not slides_path.exists():
            continue
        try:
            slides_header = get_header_from_file(slides_path)
        except NoValidHeader:
            continue

        slides_template = slides_header["template"][0]
        if slides_template != SLIDES_TEMPLATE:
            print(f"wrong template {slides_template} in {slides_path}")


def get_inclusions(filename):
    """Find inclusion filenames."""
    with open(filename, "r") as reader:
        text = reader.read()
        result = {m.group(2) for m in RE_FILE.finditer(text)}
        pats = [(m.group(1), m.group(2)) for m in RE_PAT.finditer(text)]
        for (pat, fill) in pats:
            result |= {pat.replace("*", f) for f in fill.split()}
        return result


def get_files(source_dir, dirname, unreferenced):
    """Return set of files in or below this directory."""
    if dirname == source_dir:
        candidates = set(Path(dirname).glob("*"))
    else:
        candidates = set(Path(dirname).rglob("**/*"))

    prefix_len = len(str(dirname)) + 1
    result = set(str(f)[prefix_len:] for f in candidates if f.is_file())

    ignores = set(read_directives(dirname, "unreferenced")) | unreferenced
    result = {f for f in result if not any(fnmatch(f, pat) for pat in ignores)}

    return result - EXPECTED_FILES


def get_figures(filepath):
    """Return all figures."""
    with open(filepath, "r") as reader:
        text = reader.read()
        figures = {m.group(1) for m in RE_FIGURE.finditer(text)}
        pdfs = {f.replace(".svg", ".pdf") for f in figures if f.endswith(".svg")}
        return figures | pdfs


def get_html(out_dir):
    """Get paths to HTML files for processing."""
    return list(Path(out_dir).glob("**/*.html"))


def get_links(filename):
    """Get Markdown [text][key] links from file."""
    with open(filename, "r") as reader:
        text = reader.read()
        text = RE_CODE_BLOCK.sub("", text)
        text = RE_CODE_INLINE.sub("", text)
        text = RE_SHORTCODE.sub("", text)
        return {m.group(1) for m in RE_LINK.finditer(text)}


def get_src(src_dir):
    """Get (file, dir) pairs for processing."""
    result = [(src_dir, INDEX_FILE)]
    subdirs = [s for s in Path(src_dir).iterdir() if s.is_dir()]
    return result + [(s, INDEX_FILE) for s in subdirs]


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--dom", required=True, help="DOM specification file")
    return parser.parse_args()


def read_directives(dirname, section):
    """Get a section from the directives file if it exists"""
    filepath = Path(dirname).joinpath(DIRECTIVES_FILE)
    if not filepath.exists():
        return []
    with open(filepath, "r") as reader:
        content = yaml.safe_load(reader) or {}
        return content.get(section, [])


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


def _read_html(filename):
    """Read HTML, deleting problematic code blocks if slides."""
    with open(filename, "r") as reader:
        text = reader.read()
    if SLIDES_FILE in str(filename):
        text = RE_CODE_BLOCK.sub("", text)
    return text


def _skip_dom(node):
    """Ignore this node and its children?"""
    return (
        (node.name == "div")
        and node.has_attr("class")
        and ("highlight" in node["class"])
    )


if __name__ == "__main__":
    main()
