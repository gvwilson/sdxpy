#!/usr/bin/env python

import argparse
import frontmatter
from pathlib import Path

import utils

def main():
    """Main driver."""
    options = parse_args()
    config = utils.load_config(options.config)
    chapters = set(config.chapters)
    appendices = set(config.appendices)
    needs_slides = list(sorted(chapters - appendices))
    missing_slides = [
        slug for slug in needs_slides
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
    return parser.parse_args()


if __name__ == "__main__":
    main()
