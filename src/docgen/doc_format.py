"""Format docstrings as HTML."""

import sys

import markdown
from doc_extract import Extract

# [format]
HEADING = {"module": "#", "class": "##", "function": "##"}

MISSING = "**No documentation.**"


def format(docstrings):
    """Convert dictionary of docstrings to HTML page."""
    result = []
    for key, (kind, docstring) in sorted(docstrings.items()):
        result.append(make_heading(kind, key))
        result.append(docstring if docstring is not None else MISSING)
    result = "\n\n".join(result)
    return markdown.markdown(result, extensions=["markdown.extensions.extra"])


def format_key(key):
    return key.replace(".", "-").replace("_", r"\_")


def make_heading(kind, key):
    return f"{HEADING[kind]} `{key}` {{: #{format_key(key)}}}"


# [/format]


def main(filenames):
    docstrings = Extract.extract(filenames)
    page = format(docstrings)
    print(page)


if __name__ == "__main__":
    main(sys.argv[1:])
