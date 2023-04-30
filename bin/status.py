#!/usr/bin/env python

import argparse
import re
from pathlib import Path

import frontmatter
import utils


def main():
    """Main driver."""
    options = parse_args()
    config = utils.load_config(options.config)
    report_readme(options.readme)
    report_sections(config)


def report_readme(filename):
    """Status from README file."""
    pat = re.compile(r"\|\s*(\d+)%\s*\|")
    with open(filename, "r") as reader:
        lines = reader.readlines()
        matches = [pat.search(ln) for ln in lines]
        matches = [int(m.group(1)) for m in matches if m is not None]
        percentage = int(sum(matches) / len(matches))
        print(f"Completed: {percentage}%")


def report_sections(config):
    """Status of sections."""
    chapters = set(config.chapters)
    appendices = set(config.appendices)
    needs_slides = list(sorted(chapters - appendices))
    missing_slides = [
        slug
        for slug in needs_slides
        if not Path("src", slug, "slides", "index.html").exists()
    ]
    longest = max(len(s) for s in missing_slides)
    fmt = f"{{:{longest+1}}}"
    for slug in missing_slides:
        s = fmt.format(f"{slug}:")
        title = frontmatter.load(Path("src", slug, "index.md"))["title"]
        num_files = len(list(Path("src", slug).iterdir()))
        print(f"{s} {title} ({num_files})")


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--readme", required=True, help="README file with status table")
    return parser.parse_args()


if __name__ == "__main__":
    main()
