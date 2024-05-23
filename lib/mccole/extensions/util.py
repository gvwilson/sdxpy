"""McCole template utilities."""

import ark
import collections
import markdown
from pathlib import Path
import re
import sys
import time
import yaml


# Names of parts.
KIND = {
    "en": {
        "appendix": "Appendix",
        "chapter": "Chapter",
        "defined": "Terms defined",
        "figure": "Figure",
        "table": "Table",
    },
}

# Markdown extensions.
MD_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.smarty"
]

# Match inside HTML paragraph markers.
INSIDE_PARAGRAPH = re.compile(r"<p>(.+?)</p>", re.DOTALL)

# Key for timing information.
TIMING = "__timing__"


def allowed(kwargs, allowed):
    """Check that dictionary keys are a subset of those allowed."""
    return set(kwargs.keys()).issubset(allowed)


def appendix_list(node):
    """Construct list of appendices."""
    return [
        f"<li>{cross_ref(slug, 'title')}</li>"
        for slug in ark.site.config["appendices"]
    ]


def chapter_list(node):
    """Construct list of chapters."""
    return [
        f"<li>{cross_ref(slug, 'title')}</li>"
        for slug in ark.site.config["chapters"]
    ]



def cross_ref(slug, kind):
    """Construct cross-reference."""
    if kind == "title":
        fill = ark.site.config["_meta_"][slug]["title"]
    else:
        kind = ark.site.config["_meta_"][slug]["kind"]
        number = ark.site.config["_meta_"][slug]["number"]
        fill = f"{kind}&nbsp;{number}"
    return f'<a href="@root/{slug}/">{fill}</a>'


def ensure_links():
    """Load links and create appendable text."""
    if "_links_" in ark.site.config:
        return
    filepath = Path(ark.site.home(), "info", "links.yml")
    links = yaml.safe_load(filepath.read_text()) or []
    ark.site.config["_links_"] = {lnk["key"]: lnk for lnk in links}
    ark.site.config["_links_block_"] = "\n".join(
        f"[{key}]: {value['url']}" for key, value in ark.site.config["_links_"].items()
    )


def fail(msg):
    """Fail unilaterally."""
    warn(msg)
    raise AssertionError(msg)


def get_table_slug(kwargs, filename):
    """Extract slug from kwargs or use stem of filename."""
    if "slug" in kwargs:
        return kwargs["slug"]
    require("tbl" in kwargs, f"Bad table with kwargs '{kwargs}' in {filename}")
    return str(Path(kwargs["tbl"]).stem)


def is_index_file(node):
    """Is this the main file of a section?"""
    return Path(node.filepath).name == "index.md"


def is_slide_file(node):
    """Is this the slide file of a section?"""
    return Path(node.filepath).name == "slides.md"


def kind(part_name):
    """Localize name of part."""
    lang = ark.site.config["lang"]
    require(
        part_name in KIND[lang],
        f"Unknown part name {part_name} for language {lang}",
    )
    return KIND[lang][part_name]


def load_glossary():
    """Load the glossary file."""
    if "_glossary_" not in ark.site.config:
        filepath = Path(ark.site.home(), "info", "glossary.yml")
        glossary = yaml.safe_load(filepath.read_text())
        if not glossary:
            glossary = []
        elif isinstance(glossary, dict):
            glossary = [glossary]
        else:
            assert isinstance(glossary, list)
        ark.site.config["_glossary_"] = glossary
    return ark.site.config["_glossary_"]


def markdownify(text, strip_p=True):
    """Convert Markdown to HTML."""
    result = markdown.markdown(text, extensions=MD_EXTENSIONS)
    if strip_p and result.startswith("<p>"):
        result = INSIDE_PARAGRAPH.match(result).group(1)
    return result


def require(cond, msg):
    """Fail if condition untrue."""
    if not cond:
        fail(msg)


def require_file(node, filename, kind):
    """Require that a file exists."""
    filepath = Path(Path(node.filepath).parent, filename)
    require(filepath.exists(), f"Missing {kind} file {filename} from {node.path}")


def timing(func):
    """Decorator for collecting timing information."""
    name = f"{func.__module__}.{func.__name__}"
    def _inner(*args, **kwargs):
        if TIMING not in ark.site.config:
            ark.site.config[TIMING] = collections.defaultdict(int)
        start = time.time()
        result = func(*args, **kwargs)
        ark.site.config[TIMING][name] += time.time() - start
        return result
    return _inner


def warn(msg):
    """Print warning message."""
    print(msg, file=sys.stderr)
