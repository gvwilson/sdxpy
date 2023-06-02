#!/usr/bin/env python

import argparse
import re
from pathlib import Path

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
    fmt, bar = build_format(chapters)
    s = fmt.format("Chapter")
    print(f"{s} | Slides | Exercises | Figures | Lines | Words")
    print(f"{bar} | ------ | --------- | ------- | ----- | -----")
    for slug in chapters.keys():
        with open(Path("src", slug, "index.md"), "r") as reader:
            page = reader.read()
            n_ex = count_exercises(page)
            n_fig = count_figures(page)
            n_lines = count_lines(page)
            n_words = count_words(page)
        with open(Path("src", slug, "slides.html"), "r") as reader:
            slides = reader.read()
            n_slides = count_slides(slides)
        s = fmt.format(f"{slug}")
        print(f"{s} | {n_slides:6} | {n_ex:9} | {n_fig:7} | {n_lines:5} | {n_words:5}")


def build_format(chapters):
    longest = max(len(s) for s in chapters.keys())
    longest = max(longest, len("Chapter"))
    fmt = f"{{:{longest}}}"
    return fmt, "-" * longest


def count_exercises(text):
    return len(list(RE_EXERCISE.finditer(text)))


def count_figures(text):
    return len(list(RE_FIGURE.finditer(text)))


def count_lines(text):
    return len(list(text.split("\n")))


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
