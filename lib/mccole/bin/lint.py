"""Check project."""

import argparse
import re
import sys
from fnmatch import fnmatch
from pathlib import Path

import frontmatter
import regex
import util
from bs4 import BeautifulSoup, Tag

# Required keys in configuration and their types.
CONFIG_REQUIRED = {
    "abbrev": str,
    "acknowledgments": str,
    "appendices": dict,
    "author": str,
    "bibliography": str,
    "bibliography_style": str,
    "chapters": dict,
    "copy": list,
    "credits": str,
    "debug": bool,
    "exclude": list,
    "extension": str,
    "glossary": str,
    "lang": str,
    "links": str,
    "markdown_settings": dict,
    "out_dir": str,
    "repo": str,
    "src_dir": str,
    "tagline": str,
    "theme": str,
    "title": str,
    "warnings": bool,
}

# Parts of configuration used in linting.
CONFIG_USED = [
    "appendices",
    "bibliography",
    "chapters",
    "glossary",
    "lang",
    "links",
    "src_dir",
]

# Files expected in source directories.
DIRECTIVES_FILE = ".mccole"
INDEX_FILE = "index.md"
MAKEFILE = "Makefile"
SLIDES_FILE = "slides.html"
EXPECTED_FILES = {DIRECTIVES_FILE, INDEX_FILE, MAKEFILE, SLIDES_FILE}

# Template name for slides files.
SLIDES_TEMPLATE = "slides"


def main():
    options = parse_args()
    config = get_config(options.config)

    for f in [
        check_glossary_internal,
        check_glossary_refs,
        check_glossary_redef,
        check_glossary_ref_in_index,
        check_ids,
        check_index_refs,
        check_links,
        check_inclusions,
        check_bib,
        check_slides,
    ]:
        f(config)

    check_dom(options.dom, options.pages)


def check_bib(config):
    """Check bibliography citations."""
    used = set()
    for text in config["prose"].values():
        for match in regex.BIBLIOGRAPHY_REF.finditer(text):
            for key in match.group(1).split():
                used.add(key.strip())
    unknown = used - {b for b in config["bibliography_data"].entries}
    if unknown:
        _warn("unknown bibliography keys")
        for u in unknown:
            _warn(f"- {u}")


def check_dom(dom_spec, html_files):
    """Check DOM elements in generated files."""
    allowed = util.read_yaml(dom_spec)
    seen = {}
    for filename in html_files:
        with open(filename, "r") as reader:
            text = reader.read()
        _dom_collect(seen, BeautifulSoup(text, "html.parser"))
    _dom_diff(seen, allowed)


def check_glossary_internal(config):
    """Check internal consistency of glossary."""
    # Entries missing 'key'.
    if missing_keys := [g for g in config["glossary_data"] if "key" not in g]:
        _warn(f"glossary entries without keys: {missing_keys}")
        return

    glossary = {g["key"]: g for g in config["glossary_data"]}
    for key, entry in sorted(glossary.items()):
        # Explicit cross-references.
        if "ref" in entry:
            config["glossary_refs"] |= set(entry["ref"])
            if any(missing := [ref for ref in entry["ref"] if ref not in glossary]):
                _warn(f"missing ref(s) in glossary entry {key}: {missing}")

        # No data for current language.
        if (details := entry.get(config["lang"], None)) is None:
            _warn(f"glossary entry {key} missing language {config['lang']}")

        # Term not defined for current language.
        elif "def" not in details:
            _warn(f"glossary entry {key}/{config['lang']} missing 'def'")

        # Collect internal cross-references.
        else:
            config["glossary_refs"] |= {
                m.group(1) for m in regex.GLOSSARY_CROSSREF.finditer(details["def"])
            }


def check_glossary_redef(config):
    """Check for redefinition of glossary terms."""
    seen = {}
    for slug, text in config["prose"].items():
        for match in regex.GLOSSARY_REF.finditer(text):
            key = match.group(1)
            if key not in seen:
                seen[key] = []
            seen[key].append(slug)
    problems = {
        key: occurrences
        for key, occurrences in sorted(seen.items())
        if len(occurrences) > 1
    }
    if problems:
        _warn("glossary re-definitions")
        for key, occurrences in problems.items():
            print(f"- {key}: {', '.join(occurrences)}")


def check_glossary_ref_in_index(config):
    """Check for glossary references immediately inside index references."""
    pat = re.compile(r"\[%\s*i\b.+?%\]\[%g.+?\]\[%/i%\]")
    problems = {
        slug: [m.group(0) for m in pat.finditer(text)]
        for (slug, text) in config["prose"].items()
    }
    if sum(len(prob) for prob in problems.values()):
        _warn("glossary references inside index terms")
        for slug in problems:
            if not problems[slug]:
                continue
            print(f"- {slug}")
            for p in problems[slug]:
                print(f"  - {p}")


def check_glossary_refs(config):
    """Check glossary references."""
    defined = {gl["key"] for gl in config["glossary_data"]}
    seen = config["glossary_refs"]
    for text in config["prose"].values():
        seen |= {m.group(1) for m in regex.GLOSSARY_REF.finditer(text)}
    _diff("glossary", defined, seen)


def check_ids(config):
    """Check format of anchor identifiers."""
    for kind in ["prose", "slides"]:
        for slug, text in config[kind].items():
            expected = f"{slug}-"
            figures = [
                m.group(1)
                for m in regex.FIGURE.finditer(text)
                if not m.group(1).startswith(expected)
            ]
            expected = f"#{slug}-"
            headings = [
                m.group(2)
                for m in regex.MARKDOWN_HEADING.finditer(text)
                if not m.group(2).strip().startswith(expected)
            ]
            problems = [*figures, *headings]
            if problems:
                _warn(f"Bad slugs in {slug}: {', '.join(problems)}")


def check_inclusions(config):
    """Check file inclusions."""
    for slug in config["prose"]:
        existing = get_files(config, slug)
        referenced = set()
        for text in (config["prose"][slug], config["slides"].get(slug, "")):
            for f in (get_inc, get_fig, get_img):
                referenced |= f(text)
        _diff(f"{slug} inclusions", existing, referenced)


def check_index_refs(config):
    """Check formatting of index references."""
    for slug, text in config["prose"].items():
        for match in regex.INDEX_REF.finditer(text):
            keys = match.group(1).strip()
            if not (keys.startswith('"') and keys.endswith('"')):
                _warn(f"{slug} badly-formatted index reference {match.group(0)}")


def check_links(config):
    """Check external link references."""
    defined = {ln["key"] for ln in config["links_data"] if "direct" not in ln}
    seen = set()
    for text in config["prose"].values():
        for scrub in [
            regex.MARKDOWN_CODE_BLOCK,
            regex.MARKDOWN_CODE_INLINE,
            regex.SHORTCODE,
        ]:
            text = scrub.sub("", text)
        seen |= {m.group(1) for m in regex.MARKDOWN_FOOTER_LINK.finditer(text)}
    _diff("links", defined, seen)


def check_slides(config):
    """Check slides.html files if they exist."""
    wrong = {
        slug
        for slug, text in config["slides"].items()
        if frontmatter.loads(text).get("template", None) != SLIDES_TEMPLATE
    }
    if wrong:
        _warn(f"missing/incorrect slides templates in {sorted(wrong)}")


def get_config(filepath):
    """Load and check configuration file."""
    module = util.load_config(filepath)

    for field, kind in CONFIG_REQUIRED.items():
        if field not in dir(module):
            _error(f"Configuration does not have {field}")
        elif not isinstance(getattr(module, field), kind):
            _error(f"Configuration value for {field} is not {str(kind)}")

    config = {key: getattr(module, key) for key in CONFIG_USED}
    for key in ["glossary", "links"]:
        config[f"{key}_data"] = util.read_yaml(config[key])
        config[f"{key}_refs"] = set()
    config["bibliography_data"] = util.read_bibliography(config["bibliography"])

    config["prose"] = {
        slug: _read_file(Path(config["src_dir"], slug, INDEX_FILE))
        for slug in [*config["chapters"].keys(), *config["appendices"].keys()]
    }
    config["slides"] = {
        slug: _read_file(Path(config["src_dir"], slug, SLIDES_FILE))
        for slug in config["chapters"].keys()
    }

    return config


def get_fig(text):
    """Return all figures."""
    figures = {m.group(2) for m in regex.FIGURE.finditer(text)}
    pdfs = {f.replace(".svg", ".pdf") for f in figures if f.endswith(".svg")}
    return figures | pdfs


def get_files(config, slug):
    """Return set of files in or below a source directory."""
    dir_path = Path(config["src_dir"], slug)
    candidates = set(Path(dir_path).rglob("**/*"))
    result = set(str(f.name) for f in candidates if f.is_file())
    ignores = set(_directive(dir_path, "unreferenced"))
    result = {f for f in result if not any(fnmatch(f, pat) for pat in ignores)}
    return result - EXPECTED_FILES


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


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--dom", required=True, help="DOM specification file")
    parser.add_argument("--pages", nargs="+", default=[], help="pages")
    return parser.parse_args()


def _diff(title, defined, seen):
    """Report problems."""
    for subtitle, items in [
        ("unused", defined - seen),
        ("unknown", seen - defined),
    ]:
        if not items:
            continue
        _warn(f"{title} {subtitle}")
        for i in sorted(items):
            _warn(f"- {i}")


def _directive(dir_path, section):
    """Get a section from the directives file if it exists"""
    file_path = Path(dir_path).joinpath(DIRECTIVES_FILE)
    if not file_path.exists():
        return []
    content = util.read_yaml(file_path, True)
    return content.get(section, [])


def _dom_collect(seen, node):
    """Collect DOM element attributes from given node and its descendents."""
    if not isinstance(node, Tag):
        return
    if _dom_skip(node):
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
        _dom_collect(seen, child)


def _dom_diff(actual, expected):
    """Show difference between two DOM structures."""
    for name in sorted(actual):
        if name not in expected:
            _warn(f"{name} seen but not expected")
            continue
        for attr in sorted(actual[name]):
            if attr not in expected[name]:
                _warn(f"{name}.{attr} seen but not expected")
                continue
            if expected[name][attr] == "any":
                continue
            for value in sorted(actual[name][attr]):
                if value not in expected[name][attr]:
                    _warn(f"{name}.{attr} == '{value}' seen but not expected")


def _dom_skip(node):
    """Ignore this node and its children?"""
    return (
        (node.name == "div")
        and node.has_attr("class")
        and ("highlight" in node["class"])
    )


def _error(msg):
    """Report a fatal error."""
    print(msg)
    sys.exit(1)


def _read_file(path):
    """Read a file or fail."""
    try:
        with open(path, "r") as reader:
            return reader.read()
    except FileNotFoundError:
        _error(f"file not found{str(path)}")


def _warn(msg):
    """Warn but continue."""
    print(msg)


if __name__ == "__main__":
    main()
