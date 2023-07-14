#!/usr/bin/env python

import argparse
import html
from pathlib import Path

import frontmatter
from prettytable import MARKDOWN, PrettyTable

from . import regex
from . import util

HEADINGS = (
    "title slides words sections exercises figures syllabus index glossary".split()
)
TARGETS = {
    "slides": (15, 26),
    "words": (1300, 2300),
    "sections": (2, 8),
    "exercises": (4, 14),
    "figures": (3, 8),
    "syllabus": (4, 8),
    "index": (None, None),
    "glossary": (None, None),
}
SHORT_CHAPTERS = {"intro", "finale"}


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    report(options, config.chapters)


def create_row(slug, wrap, total):
    """Create a row of the report."""
    combined = {"slides": count_slides(slug), **count_page(slug)}
    for key, val in combined.items():
        total[key] += val
    return [slug, *[wrap(slug, key, val) for (key, val) in combined.items()]]


def count_page(slug):
    """Count things in a page."""
    with open(Path("src", slug, "index.md"), "r") as reader:
        page = reader.read()
        return {
            "words": len([x for x in page.split() if x]),
            "sections": len(list(regex.MARKDOWN_H2.finditer(page))),
            "exercises": len(list(regex.EXERCISE_HEADER.finditer(page))),
            "figures": len(list(regex.FIGURE.finditer(page))),
            "syllabus": len(frontmatter.loads(page).get("syllabus", [])),
            "index": len(list(regex.INDEX_REF.finditer(page))),
            "glossary": len(list(regex.GLOSSARY_REF.finditer(page))),
        }


def count_slides(slug):
    """Count things in slides."""
    with open(Path("src", slug, "slides.html"), "r") as reader:
        text = reader.read()
        return len(list(regex.SLIDES_H2.finditer(text)))


def format_target(low, high):
    """Format the target (handling the case of none)."""
    return "" if (low is None) else f"{low}-{high}"


def get_targets(slug, key):
    """Get targets (including those for short chapters)."""
    low, high = TARGETS[key]
    if (low is not None) and (slug in SHORT_CHAPTERS):
        low, high = low / 2, high
    return low, high


def highlight_ascii(slug, key, actual):
    """Highlight as screen ASCII."""
    low, high = get_targets(slug, key)
    if (low is not None) and (actual < low):
        return f"{util.CHAR_RED}{actual}{util.CHAR_END}"
    elif (high is not None) and (actual > high):
        return f"{util.CHAR_BLUE}{actual}{util.CHAR_END}"
    else:
        return f"{util.CHAR_GREEN}{actual}{util.CHAR_END}"


def highlight_html(slug, key, actual):
    """Highlight as HTML."""
    low, high = get_targets(slug, key)
    if (low is not None) and (actual < low):
        return f'<span style="color:red">{actual}</span>'
    elif (high is not None) and (actual > high):
        return f'<span style="color:blue">{actual}</span>'
    else:
        return f'<span style="color:green">{actual}</span>'


def highlight_markdown(slug, key, actual):
    """Highlight as Markdown."""
    low, high = get_targets(slug, key)
    if (low is not None) and (actual < low):
        return f"**{actual}**"
    elif (high is not None) and (actual > high):
        return f"*{actual}*"
    else:
        return f"{actual}"


def make_table():
    """Make a pretty table object."""
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
        "--highlight",
        default=None,
        choices=["ascii", "html", "markdown"],
        help="How to highlight",
    )
    parser.add_argument("--config", required=True, help="Configuration file")
    options = parser.parse_args()
    highlighting = {
        "ascii": highlight_ascii,
        "html": highlight_html,
        "markdown": highlight_markdown,
    }
    options.highlight = highlighting.get(options.highlight, str)
    return options


def report(options, chapters):
    """Status of chapters."""
    tbl = make_table()
    total = {heading: 0 for heading in HEADINGS}
    for slug in chapters.keys():
        row = create_row(slug, options.highlight, total)
        tbl.add_row(row)
    report_summary_rows(chapters, tbl, total)
    if options.highlight == highlight_html:
        print(html.unescape(tbl.get_html_string()))
    else:
        print(tbl)


def report_summary_rows(chapters, tbl, total):
    """Add summary rows to report."""
    tbl.add_row(["---"] * len(HEADINGS))
    tbl.add_row(["Target", *[format_target(*target) for target in TARGETS.values()]])
    tbl.add_row(
        [
            "Average",
            f"{total['words']//len(chapters)}",
            *[
                f"{(val/len(chapters)):.1f}"
                for (key, val) in total.items()
                if key not in {"title", "words"}
            ],
        ]
    )
    tbl.add_row(["Total", *[count for (key, count) in total.items() if key != "title"]])


if __name__ == "__main__":
    main()
