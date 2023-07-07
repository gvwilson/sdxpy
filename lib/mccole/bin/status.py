#!/usr/bin/env python

import argparse
from collections.abc import Iterable
import frontmatter
from pathlib import Path
import regex
import util
from prettytable import MARKDOWN, PrettyTable

HEADINGS = "title slides exercises figures syllabus words".split()
TARGETS = {
    "slides": (15, 25),
    "exercises": (4, 14),
    "figures": (3, 8),
    "syllabus": (4, 8),
    "words": (1300, 2300),
}
SHORT_CHAPTERS = {"intro", "finale"}


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    report(options.highlight, config.chapters)


def calculate_fraction(slug, actual, expected):
    fraction = 100 * actual / expected
    if slug in SHORT_CHAPTERS:
        fraction *= 2
    return fraction


def create_row(slug, wrap, total):
    n_slides = count_slides(slug)
    n_exercises, n_figures, n_syllabus, n_words = count_page(slug)
    combined = (
        ("slides", n_slides),
        ("exercises", n_exercises),
        ("figures", n_figures),
        ("syllabus", n_syllabus),
        ("words", n_words),
    )
    for (key, val) in combined:
        total[key] += val
    return [
        slug,
        *[wrap(slug, key, val) for (key, val) in combined]
    ]

def count_page(slug):
    with open(Path("src", slug, "index.md"), "r") as reader:
        page = reader.read()
        return (
            len(list(regex.EXERCISE_HEADER.finditer(page))),
            len(list(regex.FIGURE.finditer(page))),
            len(frontmatter.loads(page).get("syllabus", [])),
            len([x for x in page.split() if x]),
        )


def count_slides(slug):
    with open(Path("src", slug, "slides.html"), "r") as reader:
        text = reader.read()
        lines = [s.strip() for s in text.split("\n")]
        return lines.count("---") - 2


def get_targets(slug, key):
    low, high = TARGETS[key]
    if slug in SHORT_CHAPTERS:
        low, high = low/2, high
    return low, high


def highlight_ascii(slug, key, actual):
    low, high = get_targets(slug, key)
    if actual < low:
        return f"{util.RED}{actual}{util.ENDC}"
    elif actual > high:
        return f"{util.BLUE}{actual}{util.ENDC}"
    else:
        return f"{util.GREEN}{actual}{util.ENDC}"


def highlight_html(slug, actual, expected):
    low, high = get_targets(slug, key)
    if actual < low:
        return f"**{actual}**"
    elif actual > high:
        return f"*{actual}*"
    else:
        return f"{actual}"


def make_table():
    tbl = PrettyTable()
    tbl.set_style(MARKDOWN)
    tbl.field_names = [h.title() for h in HEADINGS]
    tbl.align = "r"
    tbl.align["Title"] = "l"
    return tbl


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--highlight", default=None, choices=["ascii", "html"], help="How to highlight"
    )
    parser.add_argument("--config", required=True, help="Configuration file")
    options = parser.parse_args()
    if options.highlight == "ascii":
        options.highlight = highlight_ascii
    elif options.highlight == "html":
        options.highlight = highlight_html
    else:
        options.highlight = lambda val: f"{val}%"
    return options


def report(wrap, chapters):
    """Status of chapters."""
    tbl = make_table()
    total = {heading: 0 for heading in HEADINGS}
    for slug in chapters.keys():
        row = create_row(slug, wrap, total)
        tbl.add_row(row)
    report_summary_rows(chapters, tbl, total)
    print(tbl)


def report_summary_rows(chapters, tbl, total):
    tbl.add_row(["---"] * len(HEADINGS))
    tbl.add_row([
        "Target",
        *[f"{low}-{high}" for (low, high) in TARGETS.values()]
    ])
    tbl.add_row([
        "Average",
        *[
            f"{(val/len(chapters)):.1f}"
            for (key, val) in total.items()
            if key not in {"title", "words"}
        ],
        f"{total['words']//len(chapters)}",
    ])
    tbl.add_row([
        "Total",
        *[
            count for (key, count) in total.items()
            if key != "title"
        ]
    ])


if __name__ == "__main__":
    main()
