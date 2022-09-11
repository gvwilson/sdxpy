"""Format docstrings as HTML."""

import sys

import markdown
from markdown.extensions import Extension

from extract import Extract


HEADING = {
    "module": "#",
    "class": "##",
    "function": "##"
}

MISSING = "**No documentation.**"


def format(docstrings):
    """Convert dictionary of docstrings to HTML page."""
    result = []
    for key, (kind, docstring) in sorted(docstrings.items()):
        result.append(make_heading(kind, key))
        result.append(docstring if docstring is not None else MISSING)
    result = "\n\n".join(result)
    return markdown.markdown(result, extensions=["markdown.extensions.extra"])


def make_heading(kind, key):
    return f"{HEADING[kind]} `{key}` {{: .{key.replace('.', '-')}}}"


def main(filenames):
    docstrings = Extract.extract(filenames)
    page = format(docstrings)
    print(page)


if __name__ == "__main__":
    main(sys.argv[1:])
