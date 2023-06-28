"""Compare inclusions between prose and slides."""

import argparse
import difflib
from collections import Counter
from pathlib import Path

import regex


def main():
    """Main driver."""
    options = parse_args()
    for slug in options.chapters:
        prose = matches(Path("src", slug, "index.md"))
        duplicates(slug, "prose duplicates", prose)
        slides = matches(Path("src", slug, "slides.html"))
        duplicates(slug, "slides duplicates", slides)
        not_in_slides, out_of_order = diff(prose, slides)
        report(slug, "out of order", out_of_order)
        if options.missing:
            report(slug, "not in slides", not_in_slides)


def diff(prose, slides):
    """Slides must be subset of prose in same order."""
    prose = set(prose)
    not_in_slides = [inc for inc in slides if inc not in prose]
    in_slides = [inc for inc in slides if inc in prose]
    out_of_order = [
        inc for inc in difflib.ndiff(slides, in_slides) if not inc.startswith(" ")
    ]
    return not_in_slides, out_of_order


def duplicates(slug, title, items):
    """Find duplicated inclusions."""
    counts = Counter(items)
    dups = [key for key in counts if counts[key] > 1]
    report(slug, title, dups)


def matches(filename):
    """Get inclusions from files."""
    with open(filename, "r") as reader:
        lines = reader.readlines()
        matches = [regex.INCLUSION.match(ln) for ln in lines]
        return [m.group(1) for m in matches if m is not None]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapters", nargs="+", default=[], help="chapter slugs")
    parser.add_argument(
        "--missing", action="store_true", default=False, help="report missing"
    )
    return parser.parse_args()


def report(slug, title, items):
    """Show results."""
    if not items:
        return
    print(f"{slug} {title}:")
    for i in items:
        print(i)


if __name__ == "__main__":
    main()
