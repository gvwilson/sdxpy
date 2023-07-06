#!/usr/bin/env python

import argparse
from collections.abc import Iterable
import frontmatter
from pathlib import Path
import regex
import util
from prettytable import MARKDOWN, PrettyTable

EXERCISES_PER = 5
FIGURES_PER = 4
SLIDES_PER = 18
SYLLABUS_PER = 5
WORDS_PER = 2200
THRESHOLD_LOW = 80
THRESHOLD_HIGH = 200
SHORT_CHAPTERS = {"intro", "finale"}
HEADINGS = "title slides exercises figures syllabus words".split()


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    report(options.highlight, config.chapters)


def build_format(chapters):
    longest = max("title", *[len(s) for s in chapters.keys()])
    fmt = f"{{:{longest}}}"
    return fmt, "-" * longest


def calculate_fraction(slug, actual, expected):
    fraction = 100 * actual / expected
    if slug in SHORT_CHAPTERS:
        fraction *= 2
    return fraction


def create_row(slug, wrap, total):
    n_slides = count_slides(slug)
    n_ex, n_fig, n_syll, n_words = count_page(slug)
    combined = (
        ("slides", n_slides, SLIDES_PER),
        ("exercises", n_ex, EXERCISES_PER),
        ("figures", n_fig, FIGURES_PER),
        ("syllabus", n_syll, SYLLABUS_PER),
        ("words", n_words, WORDS_PER),
    )
    for (key, val, _) in combined:
        total[key] += val
    return [
        slug,
        *[wrap(slug, val, expected) for (_, val, expected) in combined]
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


def highlight_ascii(slug, actual, expected):
    fraction = calculate_fraction(slug, actual, expected)
    if fraction < THRESHOLD_LOW:
        return f"{util.RED}{actual}{util.ENDC}"
    elif fraction > THRESHOLD_HIGH:
        return f"{util.BLUE}{actual}{util.ENDC}"
    else:
        return f"{util.GREEN}{actual}{util.ENDC}"


def highlight_html(slug, actual, expected):
    fraction = calculate_fraction(slug, actual, expected)
    if slug in SHORT_CHAPTERS:
        fraction *= 2
    if fraction < 80:
        return f"**{actual}**"
    elif fraction > 120:
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
        SLIDES_PER,
        EXERCISES_PER,
        FIGURES_PER,
        SYLLABUS_PER,
        WORDS_PER,
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
