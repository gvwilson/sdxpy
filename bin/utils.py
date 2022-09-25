"""Utilities used across all tools."""


import re
import sys

import yaml

# Width of output lines in included chunks.
WIDTH = 72

# Length of included chunks.
LENGTH = 30

# Known languages.
LANGUAGES = {"html", "js", "make", "out", "py", "sh", "txt", "yml"}

# Multiple consecutive whitespace characters.
WHITESPACE = re.compile(r"\s+")

# Glossary references use <span g="...">...</span>.
GLOSS_REF = re.compile(r'<span[^>]+g="(.+?)"[^>]*>', re.DOTALL)

# Index references use <span i="...">...</span>.
INDEX_REF = re.compile(r'<span[^>]+i="(.+?)"[^>]*>', re.DOTALL)

# Citations use <cite>key,key</cite>.
CITATION = re.compile(r"<cite>(.+?)</cite>", re.DOTALL)

# Patterns to remove from input when tokenizing Markdown source files.
ALWAYS = [
    re.compile(r"---"),  # em-dashes
    re.compile(r"[©×±μ…\(\);:]"),  # strange characters and punctuation
    re.compile(r"```.+?```", re.DOTALL),  # code blocks
    re.compile(r"`.+?`", re.DOTALL),  # inline code
    re.compile(r"{%\s+raw\s+%}.*?{%\s+endraw\s+%}", re.DOTALL),  # raw blocks
    re.compile(r'<div\s+class="callout"\s*markdown="1">'),  # opening callout
    re.compile(r"</div>"),  # closing callout
    re.compile(r"<http.+?>"),
]
SCRUB = [
    re.compile(r"{%\s+include\s+.+?%}", re.DOTALL),  # inclusions
    re.compile(r"{:\s+.continue\s*}", re.DOTALL),  # continued paragraphs
    re.compile("<code>"),  # start code
    re.compile("</code>"),  # end code
    re.compile("<em>"),  # start emphasis
    re.compile("</em>"),  # end emphasis
    re.compile("<blockquote>"),  # start quotation
    re.compile("</blockquote>"),  # end quotation
]

# Width of YAML dumps.
YAML_INFINITE = 100000

# Characters to replace in YAML dumps.
YAML_CHARACTERS = {
    r"\u0103": "ă",
    r"\u2014": "—",
    r"\u2026": "…",
    r"\xB0": "°",
    r"\xC5": "Å",
    r"\xE1": "á",
    r"\xE9": "é",
    r"\xF3": "ó",
    r"\xF6": "ö",
}


def cook_yaml(text, doublespace_keys=True):
    """Fix text produced by converting YAML to text."""
    for src in YAML_CHARACTERS:
        text = text.replace(src, YAML_CHARACTERS[src])
    if doublespace_keys:
        text = text.replace("- key:", "\n- key:").lstrip()
    return text


def get_all_matches(pattern, filenames, group=1, scrub=True, no_duplicates=False):
    """Create set of matches in source files."""
    result = set()
    for filename in filenames:
        duplicates = []
        result |= get_matches(pattern, filename, group, scrub, duplicates)
        if duplicates and no_duplicates:
            print(f"** duplicate key(s) {duplicates} **", file=sys.stderr)
    return result


def get_entry_info(config):
    """Return dictionary of {slug, title, file, kind, label} for all chapters."""
    num_chapters = None
    kind = "Chapter"
    result = []
    for (i, entry) in enumerate(config["chapters"]):
        if "appendix" in entry:
            num_chapters = i + 1
            kind = "Appendix"
            continue
        title = entry["title"]
        slug = entry["slug"]
        filename = entry["file"] if ("file" in entry) else f'./{entry["slug"]}/index.md'
        label = f"{i+1}" if (num_chapters is None) else chr(ord("A") + i - num_chapters)
        result.append(
            {
                "slug": slug,
                "title": title,
                "file": filename,
                "kind": kind,
                "label": label,
            }
        )
    return result


def get_matches(pattern, filename, group=1, scrub=True, duplicates=None, split=","):
    """Get matches from a single file."""
    result = set()
    text = read_file(filename, scrub)
    for match in pattern.finditer(text):
        words = match.group(group)
        words = words.split(split) if split else [words]
        for word in words:
            if (duplicates is not None) and (word in result):
                duplicates.append(word)
            result.add(word.strip())
    return result


def read_file(filename, scrub=True):
    """Read a file, removing raw sections if requested."""
    with open(filename, "r") as reader:
        text = reader.read()
        for pattern in ALWAYS:
            text = pattern.sub(" ", text)
        if scrub:
            for pattern in SCRUB:
                text = pattern.sub(" ", text)
        return text


def read_yaml(filename):
    """Load and return a YAML file."""
    with open(filename, "r") as reader:
        return yaml.load(reader, Loader=yaml.FullLoader)


def report(title, checkOnlyRight=True, **kwargs):
    """Report items if present."""
    assert len(kwargs) == 2, "Must have two sets to report"
    left, right = kwargs.keys()
    onlyLeft = kwargs[left] - kwargs[right]
    onlyRight = kwargs[right] - kwargs[left]
    if onlyLeft or (checkOnlyRight and onlyRight):
        print(f"- {title}")
        if onlyLeft:
            print(f"  - {left} but not {right}")
            for item in sorted(onlyLeft):
                print(f"    - {item}")
        if checkOnlyRight and onlyRight:
            print(f"  - {right} but not {left}")
            for item in sorted(onlyRight):
                print(f"    - {item}")


def strip_nested(value):
    """Strip a string or all strings in a list."""
    if type(value) == str:
        return value.strip()
    elif type(value) == list:
        return [x.strip() for x in value]
    return value


def write_yaml(filename, data):
    """Save a YAML file."""
    with open(filename, "w") as writer:
        return yaml.dump(data, writer)
