#!/usr/bin/env python

import argparse
import re
from pathlib import Path
from prettytable import PrettyTable, MARKDOWN

import utils

RE_EXERCISE = re.compile(r"\{:\s+\.exercise\}")
RE_FIGURE = re.compile(r"\[%\s*figure\b")
RE_STATUS = re.compile(r"\|\s*\*?(\d+)%\*?\s*\|")

EX_PER_CHAPTER = 8
SLIDES_PER_CHAPTER = 18
WORDS_PER_CHAPTER = 2200


def main():
    """Main driver."""
    options = parse_args()
    config = utils.load_config(options.config)
    report(config.chapters)


def build_format(chapters):
    longest = max(len(s) for s in chapters.keys())
    longest = max(longest, len("Chapter"))
    fmt = f"{{:{longest}}}"
    return fmt, "-" * longest


def calc_fraction(n_slides, n_ex, n_words):
    entries = ((n_slides, SLIDES_PER_CHAPTER),
               (n_ex, EX_PER_CHAPTER),
               (n_words, WORDS_PER_CHAPTER))
    frac = sum(entry[0]/entry[1] for entry in entries)
    return int(100 * frac / len(entries))


def count_page(slug):
    with open(Path("src", slug, "index.md"), "r") as reader:
        page = reader.read()
        return count_re(RE_EXERCISE, page), count_re(RE_FIGURE, page), count_words(page)


def count_re(pat, text):
    return len(list(pat.finditer(text)))


def count_slides(slug):
    with open(Path("src", slug, "slides.html"), "r") as reader:
        text = reader.read()
        lines = [s.strip() for s in text.split("\n")]
        return lines.count("---") - 2


def count_words(text):
    return len([x for x in text.split() if x])


def make_table():
    tbl = PrettyTable()
    tbl.set_style(MARKDOWN)
    tbl.field_names = "Chapter Slides Exercises Figures Words Status".split()
    tbl.align = "r"
    tbl.align["Chapter"] = "l"
    return tbl


def overall(chapters, n_slides, n_ex, n_words):
    n_chapters = len(chapters) - 1 # intro and conclusion count as 1
    frac = calc_fraction(n_slides, n_ex, n_words)
    return int(frac / n_chapters)


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--readme", required=True, help="README file with status table")
    return parser.parse_args()


def report(chapters):
    """Status of chapters."""
    tbl = make_table()
    tot_slides, tot_ex, tot_words = 0, 0, 0
    for slug in chapters.keys():
        n_ex, n_fig, n_words = count_page(slug)
        n_slides = count_slides(slug)
        tot_ex += n_ex
        tot_slides += n_slides
        tot_words += n_words
        frac = f"{calc_fraction(n_slides, n_ex, n_words)}%"
        tbl.add_row([slug, n_slides, n_ex, n_fig, n_words, frac])
    print(f"Overall: {overall(chapters, tot_slides, tot_ex, tot_words)}%")
    print(tbl)


if __name__ == "__main__":
    main()
