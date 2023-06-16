#!/usr/bin/env python

"""Check project."""


import argparse
import sys
from fnmatch import fnmatch
from pathlib import Path

import regex
import utils
import yaml
from bs4 import BeautifulSoup, Tag
from yaml_header_tools import NoValidHeader, get_header_from_file

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

DIRECTIVES_FILE = ".mccole"
INDEX_FILE = "index.md"
MAKEFILE = "Makefile"
SLIDES_FILE = "slides.html"
SLIDES_TEMPLATE = "slides"
EXPECTED_FILES = {DIRECTIVES_FILE, INDEX_FILE, MAKEFILE, SLIDES_FILE}


def main():
    """Main driver."""
    options = parse_args()

    config = check_config(options.config)
    language = getattr(config, "lang")
    src_dir = getattr(config, "src_dir")
    slugs = get_slugs(config)
    glossary = utils.read_yaml(getattr(config, "glossary"))

    if not check_dirs(src_dir, slugs):
        sys.exit(1)

    cross_refs = check_glossary(glossary, language)
    check_files(src_dir, slugs, glossary, cross_refs)
    check_dom(options.dom, options.pages)


def check_config(config_path):
    """Check configuration file."""

    def _require(m, field, kind):
        if field not in dir(m):
            print(f"Configuration does not have {field}")
        elif not isinstance(getattr(m, field), kind):
            print(f"Configuration value for {field} is not {str(kind)}")

    module = utils.load_config(config_path)
    for field, kind in CONFIGURATION:
        _require(module, field, kind)

    return module


def check_dirs(src_dir, slugs):
    """Make sure source directores are present."""
    expected = {str(Path(src_dir, s)) for s in slugs}
    actual = {str(d) for d in Path(src_dir).iterdir()} - {
        str(Path(src_dir, "index.md"))
    }
    if expected == actual:
        return True
    print("slug/directory mis-match", expected.symmetric_difference(actual))
    return False


def check_dom(dom_spec, html_files):
    """Check DOM elements in generated files."""
    allowed = utils.read_yaml(dom_spec)
    seen = {}
    for filename in html_files:
        text = _read_html(filename)
        dom = BeautifulSoup(text, "html.parser")
        _collect_dom(seen, dom)
    _diff_dom(seen, allowed)


def check_files(src_dir, slugs, glossary, cross_refs):
    """Check for inclusions, figures, and glossary references."""
    gloss_keys = {entry["key"] for entry in glossary}
    gloss_unused = gloss_keys.copy() - cross_refs
    for slug in slugs:
        dir_path = Path(src_dir, slug)
        text = read_prose(dir_path)
        slides = read_slides(dir_path)

        referenced = set()
        for source in (text, slides):
            for func in (get_inc, get_fig, get_img):
                referenced |= func(source)
        existing = get_files(dir_path)
        report(f"{dir_path}: inclusions", referenced, existing)

        referenced = get_glossrefs(text)
        report_one(f"{dir_path}: glossary", referenced - gloss_keys)
        gloss_unused -= referenced
    if gloss_unused:
        print("glossary unused:")
        for key in sorted(gloss_unused):
            print(f"- {key}")


def check_glossary(glossary, language):
    """Check internal consistency of glossary."""
    missing_keys = [g for g in glossary if "key" not in g]
    if missing_keys:
        print(f"glossary entries without keys: {missing_keys}")
        return

    glossary = {g["key"]: g for g in glossary}
    cross_refs = set()
    for key, entry in sorted(glossary.items()):
        if "ref" in entry:
            missing = [ref for ref in entry["ref"] if ref not in glossary]
            if any(missing):
                print(f"missing ref(s) in glossary entry {key}: {missing}")
        if language not in entry:
            print(f"glossary entry {key} missing {language}")
            break
        if "def" not in entry[language]:
            print(f"glossary entry {key}/{language} missing 'def'")
            break
        cross_refs |= {
            m.group(1) for m in regex.GLOSSARY_CROSSREF.finditer(entry[language]["def"])
        }
    return cross_refs


def check_links(links, source_files):
    """Check that all links are known."""
    existing = {entry["key"] for entry in links if not entry.get("direct", False)}
    referenced = set()
    for dirname, filename in source_files:
        referenced |= get_links(Path(dirname, filename))
    report("links", referenced, existing)


def check_slides(source_files):
    """Check slides.html files if they exist."""
    for dir_path, index_file in source_files:
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


def get_files(dir_path):
    """Return set of files in or below this directory."""
    candidates = set(Path(dir_path).rglob("**/*"))
    result = set(str(f.name) for f in candidates if f.is_file())
    ignores = set(read_directives(dir_path, "unreferenced"))
    result = {f for f in result if not any(fnmatch(f, pat) for pat in ignores)}
    return result - EXPECTED_FILES


def get_fig(text):
    """Return all figures."""
    figures = {m.group(1) for m in regex.FIGURE.finditer(text)}
    pdfs = {f.replace(".svg", ".pdf") for f in figures if f.endswith(".svg")}
    return figures | pdfs


def get_glossrefs(text):
    """Return all glossary reference keys."""
    return {m.group(1) for m in regex.GLOSSARY_REF.finditer(text)}


def get_img(text):
    """Find direct image references."""
    return {m.group(1) for m in regex.IMG.finditer(text)}


def get_inc(text):
    """Find inclusion filenames."""
    result = {m.group(2) for m in regex.INCLUSION_FILE.finditer(text)}
    pats = [(m.group(1), m.group(2)) for m in regex.INCLUSION_PAT.finditer(text)]
    for pat, fill in pats:
        result |= {pat.replace("*", f) for f in fill.split()}
    return result


def get_links(filename):
    """Get Markdown [text][key] links from file."""
    with open(filename, "r") as reader:
        text = reader.read()
        text = regex.MARKDOWN_CODE_BLOCK.sub("", text)
        text = regex.MARKDOWN_CODE_INLINE.sub("", text)
        text = regex.SHORTCODE.sub("", text)
        return {m.group(1) for m in regex.MARKDOWN_FOOTER_LINK.finditer(text)}


def get_slugs(config):
    """Get chapter and appendix slugs in order."""
    return list(getattr(config, "chapters").keys()) + list(
        getattr(config, "appendices").keys()
    )


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
    parser.add_argument("--pages", nargs="+", default=[], help="pages")
    return parser.parse_args()


def read_directives(dirname, section):
    """Get a section from the directives file if it exists"""
    filepath = Path(dirname).joinpath(DIRECTIVES_FILE)
    if not filepath.exists():
        return []
    with open(filepath, "r") as reader:
        content = yaml.safe_load(reader) or {}
        return content.get(section, [])


def read_prose(dir_path):
    """Read prose in index file."""
    file_path = Path(dir_path, "index.md")
    with open(file_path, "r") as reader:
        return reader.read()


def read_slides(dir_path):
    slides_path = Path(dir_path, "slides.html")
    if not slides_path.is_file():
        return ""
    with open(slides_path, "r") as reader:
        return reader.read()


def report(title, expected, actual):
    """Report problems."""
    if expected == actual:
        return
    print(title)
    for subtitle, items in [
        ("missing", expected - actual),
        ("extra", actual - expected),
    ]:
        if not items:
            continue
        print(f"- {subtitle}")
        for i in sorted(items):
            print(f"  - {i}")


def report_one(title, items):
    """Report single-sided problems."""
    if not items:
        return
    print(title)
    for i in sorted(items):
        print(f"- {i}")


def _collect_dom(seen, node):
    """Collect DOM element attributes from given node and its descendents."""
    if not isinstance(node, Tag):
        return
    if _skip_dom(node):
        return
    if node.name not in seen:
        seen[node.name] = {}
    for key, value in node.attrs.items():
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
