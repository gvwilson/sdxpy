#!/usr/bin/env python

import argparse
import re
from pathlib import Path

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
    longest = max(len(s) for s in config.chapters.keys())
    fmt = f"{{:{longest+1}}}"
    for slug in config.chapters.keys():
        num = count_slides(Path("src", slug, "slides.html"))
        s = fmt.format(f"{slug}:")
        print(f"{s} {num:2}")


def count_slides(filename):
    with open(filename, "r") as reader:
        lines = [s.strip() for s in reader.readlines()]
        return lines.count("---") - 2


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--readme", required=True, help="README file with status table")
    return parser.parse_args()


if __name__ == "__main__":
    main()
