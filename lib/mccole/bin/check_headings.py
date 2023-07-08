"""Checking casing of titles."""

import argparse
from pathlib import Path

import regex
import util

# Stop-words in headings.
STOP_WORDS = {"a", "and", "as", "in", "of", "or", "to", "the"}


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    prose = {
        slug: open(Path(config.src_dir, slug, "index.md")).read()
        for slug in [*config.chapters.keys(), *config.appendices.keys()]
    }
    check_heading_case(prose)


def check_heading_case(prose):
    """Check title-casing of all headings."""
    for slug, text in prose.items():
        headings = [
            *[m.group(1) for m in regex.MARKDOWN_H2.finditer(text)],
            *[m.group(1) for m in regex.MARKDOWN_H3.finditer(text)],
        ]
        stripped = {h: strip_heading(h) for h in headings}
        problems = [h for (h, s) in stripped.items() if s.title() != s]
        if problems:
            print(f"{slug} headings: {', '.join(problems)}")


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    return parser.parse_args()


def strip_heading(heading):
    """Remove stop-words from heading."""
    heading = heading.split()
    return " ".join(h for h in heading if h not in STOP_WORDS)


if __name__ == "__main__":
    main()
