#!/usr/bin/env python

import argparse
import re
from pathlib import Path
from prettytable import PrettyTable

import utils

RE_EXERCISE = re.compile(r"\{:\s+\.exercise\}")
RE_FIGURE = re.compile(r"\[%\s*figure\b")
RE_STATUS = re.compile(r"\|\s*\*?(\d+)%\*?\s*\|")


def main():
    """Main driver."""
    options = parse_args()
    config = utils.load_config(options.config)
    report_readme(options.readme)
    report_chapters(config.chapters)


def report_readme(filename):
    """Status from README file."""
    with open(filename, "r") as reader:
        lines = reader.readlines()
        matches = [RE_STATUS.search(ln) for ln in lines]
        matches = [int(m.group(1)) for m in matches if m is not None]
        percentage = int(sum(matches) / len(matches))
        print(f"Completed: {percentage}%")


def report_chapters(chapters):
    """Status of chapters."""
    tbl = PrettyTable()
    tbl.field_names = "Chapter Slides Exercises Figures Lines Words".split()
    tbl.align = "r"
    tbl.align["Chapter"] = "l"
    for slug in chapters.keys():
        with open(Path("src", slug, "index.md"), "r") as reader:
            page = reader.read()
            n_ex = count_re(RE_EXERCISE, page)
            n_fig = count_re(RE_FIGURE, page)
            n_lines = page.count("\n")
            n_words = count_words(page)
        with open(Path("src", slug, "slides.html"), "r") as reader:
            slides = reader.read()
            n_slides = count_slides(slides)
        tbl.add_row([slug, n_slides, n_ex, n_fig, n_lines, n_words])
    print(tbl)


def build_format(chapters):
    longest = max(len(s) for s in chapters.keys())
    longest = max(longest, len("Chapter"))
    fmt = f"{{:{longest}}}"
    return fmt, "-" * longest


def count_re(pat, text):
    return len(list(pat.finditer(text)))


def count_slides(text):
    lines = [s.strip() for s in text.split("\n")]
    return lines.count("---") - 2


def count_words(text):
    return len([x for x in text.split() if x])


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--readme", required=True, help="README file with status table")
    return parser.parse_args()


if __name__ == "__main__":
    main()
