"""Regenerate GitHub root pages."""

import argparse
import sys

from . import regex
from . import util

CHANGES = [
    (regex.MARKDOWN_H2, lambda m: f"## {m.group(1)}\n"),
    (regex.PARAGRAPH_CONTINUE, ""),
    (regex.GITHUB_ISSUE, lambda m: f"#{m.group(1)}"),
    (regex.BIBLIOGRAPHY_REF, lambda m: f"[{m.group(1)}]"),
]


def main():
    """Main driver."""
    options = parse_args()

    text = read_text(options)
    for pat, sub in CHANGES:
        text = pat.sub(sub, text)

    links = util.read_yaml(options.links)
    links = {ln["key"]: ln["url"] for ln in links}

    needed = {m.group(1) for m in regex.MARKDOWN_FOOTER_LINK.finditer(text)}
    needed = {key: links[key] for key in sorted(needed) if key in links}

    print(f"# {options.title}\n")
    print(text)
    for key, url in needed.items():
        print(f"[{key}]: {url}")


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--append", required=False, help="Text to append")
    parser.add_argument("--links", required=True, help="Links file")
    parser.add_argument("--title", required=True, help="Page title")
    parser.add_argument("--source", required=False, help="Source page")
    return parser.parse_args()


def read_text(options):
    if options.source:
        with open(options.source, "r") as reader:
            text = reader.read()
    else:
        text = sys.stdin.read()

    if options.append is not None:
        with open(options.append, "r") as reader:
            text += "\n"
            text += reader.read()

    return text


if __name__ == "__main__":
    main()
