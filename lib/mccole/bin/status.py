#!/usr/bin/env python

import argparse
import re
from pathlib import Path

import utils


RE_EXERCISE = re.compile(r"\{:\s+\.exercise\}")
RE_STATUS = re.compile(r"\|\s*(\d+)%\s*\|")


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
    """Status of sections."""
    longest = max(len(s) for s in chapters.keys())
    longest = max(longest, len("Chapter"))
    fmt = f"{{:{longest}}}"
    s = fmt.format("Chapter")
    print(f"{s} | Slides | Exercises | Lines")
    s = fmt.format("-" * longest)
    print(f"{s} | ------ | --------- | -----")
    for slug in chapters.keys():
        page = Path("src", slug, "index.md")
        slides = Path("src", slug, "slides.html")
        num_exercises = count_exercises(page)
        num_lines = count_lines(page)
        num_slides = count_slides(slides)
        s = fmt.format(f'{slug}')
        print(f"{s} | {num_slides:6} | {num_exercises:9} | {num_lines:5}")


def count_exercises(filename):
    with open(filename, "r") as reader:
        return len(list(RE_EXERCISE.finditer(reader.read())))


def count_lines(filename):
    with open(filename, "r") as reader:
        return len(list(reader.readlines()))


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
