"""Compare inclusions between prose and slides."""

import argparse
import re
import utils
from pathlib import Path
import difflib


RE_INCLUSION = re.compile(r'(\[%\s+inc.+?%\])')


def main():
    """Main driver."""
    options = parse_args()
    for slug in options.pages:
        in_prose = get_matches(Path("src", slug, "index.md"))
        in_slides = get_matches(Path("src", slug, "slides.html"))
        diff = list(difflib.ndiff(in_prose, in_slides))
        if diff:
            print(f"## {slug}")
            for line in diff:
                print(line)


def get_matches(filename):
    with open(filename, "r") as reader:
        lines = reader.readlines()
        matches = [RE_INCLUSION.match(ln) for ln in lines]
        return [m.group(1) for m in matches if m is not None]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", nargs="+", default=[], help="pages")
    return parser.parse_args()


if __name__ == "__main__":
    main()
