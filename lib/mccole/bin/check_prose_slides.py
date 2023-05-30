"""Check prose and slides against each other."""

import argparse
import re
from difflib import Differ
from pathlib import Path

import utils

PAT_CODE = re.compile(r"\[%\s*inc\b([^%]+)%\]")


def main():
    """Main driver."""
    options = parse_args()
    config = utils.load_config(options.config)
    problems = {slug: compare(slug) for slug in config.chapters}
    report(problems)


def compare(slug):
    """Compare prose and slides for a chapter."""
    try:
        prose = open(Path("src", slug, "index.md"), "r").read()
        slides = open(Path("src", slug, "slides", "index.html"), "r").read()
    except FileNotFoundError:
        return ""
    prose_code = list(m.group(1).strip() for m in PAT_CODE.finditer(prose))
    slides_code = list(m.group(1).strip() for m in PAT_CODE.finditer(slides))
    return list(Differ().compare(prose_code, slides_code))


def parse_args():
    """Handle command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="configuration file")
    return parser.parse_args()


def report(problems):
    """Print report."""
    for slug, diff in problems.items():
        if not diff:
            continue
        print(f"=== {slug}")
        for ln in diff:
            print(ln)


if __name__ == "__main__":
    main()
