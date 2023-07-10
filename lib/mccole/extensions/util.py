"""Utilities."""

import os
import sys
from pathlib import Path

import ark
import markdown
import yaml
from pybtex.database import parse_file

# File containing things to ignore.
DIRECTIVES_FILE = ".mccole"

# Configuration sections and their default values.
# These are added to the config dynamically under the `mccole` key,
# i.e., `"figures"` becomes `ark.site.config["mccole"]["figures"]`.
CONFIGURATIONS = {
    "bibliography": set(),  # citations
    "figures": {},  # numbered figures
    "glossary_by_key": {},  # glossary definitions by key for current language
    "glossary_in_chapter": [],  # glossary definitions used per chapter
    "glossary_keys_used": set(),  # glossary keys seen overall
    "headings": {},  # number chapter, section, and appendix headings
    "inclusions": {},  # included files
    "index": {},  # index entries
    "syllabus": [],  # syllabus entries
    "tables": {},  # numbered tables
    "titles": {},  # chapter and appendix titles in order
}

# Translations of multilingual terms.
TRANSLATIONS = {
    "en": {
        "appendix": "Appendix",
        "chapter": "Chapter",
        "figure": "Figure",
        "issue": "issue",
        "seealso": "See also",
        "section": "Section",
        "table": "Table",
    },
    "es": {
        "appendix": "Anexo",
        "chapter": "Capítulo",
        "figure": "Figura",
        "issue": "problema",
        "seealso": "Ver también",
        "section": "Sección",
        "table": "Tabla",
    },
}

# Cached values.
CACHE = {
    "glossary": None,
    "glossary_by_key": None,
    "links": None,
    "links_table": None,
    "major": None,
    "titles": None,
}


def fail(msg):
    """Fail unilaterally."""
    print(msg, file=sys.stderr)
    raise AssertionError(msg)


def get_config(part):
    """Get configuration subsection or `None`.

    A result of `None` indicates the request is being made too early
    in the processing cycle.
    """
    require(part in CONFIGURATIONS, f"Unknown configuration section '{part}'")
    mccole = ark.site.config.setdefault("mccole", {})
    return mccole.get(part, None)


def get_chapter_slug(node):
    """Get chapter-level slug of index files or slides file, or None."""
    if is_slides(node):
        require(len(node.path) > 1, f"Bad path {node.path} for slides")
        return node.path[-2]
    return node.path[-1]


def get_title(node):
    """Get chapter/appendix title from configuration."""
    if CACHE["titles"] is None:
        CACHE["titles"] = {
            **ark.site.config["chapters"],
            **ark.site.config["appendices"],
        }
    slug = get_chapter_slug(node)
    require(slug in CACHE["titles"], f"Unknown slug {slug} for titles in {node}")
    return CACHE["titles"][slug]


def is_slides(node):
    """Is this a slides file?"""
    return "slides" in node.get_template_list()


def make_config(part, filler=None):
    """Make configuration subsection.

    If `filler` is provided, it is used as the initial value.
    Otherwise, the value from `CONFIGURATIONS` is used.
    """
    require(part in CONFIGURATIONS, f"Unknown configuration section '{part}'")
    filler = filler if (filler is not None) else CONFIGURATIONS[part]
    return ark.site.config.setdefault("mccole", {}).setdefault(part, filler)


def make_copy_paths(node, filename, original=None, replacement=None):
    """Make source and destination paths for copying."""
    if (original is not None) and filename.endswith(original):
        filename = filename.replace(original, replacement)
    src = os.path.join(os.path.dirname(node.filepath), filename)
    dst = os.path.join(os.path.dirname(node.get_output_filepath()), filename)
    return src, dst


def make_label(kind, number):
    """Create numbered labels for figures, tables, and document parts."""
    translations = TRANSLATIONS[ark.site.config["lang"]]
    if kind == "figure":
        name = translations["figure"]
    elif kind == "part":
        if len(number) > 1:
            name = translations["section"]
        elif number[0].isdigit():
            name = translations["chapter"]
        else:
            name = translations["appendix"]
    elif kind == "table":
        name = translations["table"]
    else:
        fail(f"Unknown kind of label {kind}")

    number = ".".join(number)
    return f"{name} {number}"


def make_links_table():
    """Make a table of links for inclusion in Markdown."""
    if CACHE["links_table"] is None:
        links = read_links()
        CACHE["links_table"] = "\n".join([f"[{x['key']}]: {x['url']}" for x in links])
    return CACHE["links_table"]


def make_major_numbering():
    """Construct major numbers/letters based on configuration.

    This function relies on the configuration containing `"chapters"`
    and `"appendices"`, which must be lists of slugs.
    """
    if CACHE["major"] is None:
        chapters = {slug: i + 1 for (i, slug) in enumerate(ark.site.config["chapters"])}
        appendices = {
            slug: chr(ord("A") + i)
            for (i, slug) in enumerate(ark.site.config["appendices"])
        }
        CACHE["major"] = chapters | appendices
    return CACHE["major"]


def markdownify(text, ext=None, strip=True):
    """Convert to Markdown."""
    extensions = ["markdown.extensions.extra", "markdown.extensions.smarty"]
    if ext:
        extensions = [ext, *extensions]
    result = markdown.markdown(text, extensions=extensions)
    if strip and result.startswith("<p>"):
        result = result[3:-4]  # remove trailing '</p>' as well
    return result


def mccole():
    """Get configuration section, creating if necessary."""
    return ark.site.config.setdefault("mccole", {})


def read_bibliography(filename):
    """Read BibTeX bibliography."""
    return parse_file(filename)


def read_directives(dirname, section):
    """Get a section from the directives file if it exists"""
    filepath = Path(dirname).joinpath(DIRECTIVES_FILE)
    if not filepath.exists():
        return []
    with open(filepath, "r") as reader:
        content = yaml.safe_load(reader) or {}
        return content.get(section, [])


def read_glossary():
    """Load the glossary definitions."""
    lang = ark.site.config.get("lang", None)
    require(lang is not None, "No language specified")

    if CACHE["glossary"] is None:
        filename = ark.site.config.get("glossary", None)
        require(filename is not None, "No glossary specified")
        filename = Path(ark.site.home(), filename)
        with open(filename, "r") as reader:
            glossary = yaml.safe_load(reader) or []

        for entry in glossary:
            assert lang in entry, f"Bad glossary entry {entry}"
            assert "def" in entry[lang], f"Bad glossary entry {entry}"
        CACHE["glossary"] = glossary
        make_config(
            "glossary_by_key", {entry["key"]: entry[lang] for entry in glossary}
        )

    return CACHE["glossary"], lang


def read_links():
    """Read links file."""
    if CACHE["links"] is None:
        filepath = Path(ark.site.home(), ark.site.config["links"])
        with open(filepath, "r") as reader:
            CACHE["links"] = yaml.safe_load(reader)
    return CACHE["links"]


def read_thanks():
    """Load the thanks definitions."""
    filename = Path(ark.site.home(), ark.site.config["thanks"])
    with open(filename, "r") as reader:
        return yaml.safe_load(reader) or []


def require(cond, msg):
    """Fail if condition untrue."""
    if not cond:
        fail(msg)


def require_file(node, filename, kind):
    """Require that a file exists."""
    directory = Path(node.filepath).parent
    filepath = Path(directory, filename)
    msg = f"Missing {kind} file {filename} from {node}"
    require(filepath.exists(), msg)


def warn(title, items):
    """Warn about missing or unused items."""
    if not ark.site.config.get("warnings", False):
        return
    if not items:
        return
    print(title)
    for i in sorted(items):
        print(f"-  {i}")
