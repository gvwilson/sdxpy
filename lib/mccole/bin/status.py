#!/usr/bin/env python

import argparse
from pathlib import Path

import regex
import util
from prettytable import MARKDOWN, PrettyTable

EXERCISES_PER = 8
SLIDES_PER = 18
WORDS_PER = 2200
THRESHOLD_LOW = 80
THRESHOLD_HIGH = 120

SHORT_CHAPTERS = {"intro", "finale"}


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    wrapper = choose_wrapper(options)
    report(wrapper, config.chapters)


def build_format(chapters):
    longest = max(len(s) for s in chapters.keys())
    longest = max(longest, len("Chapter"))
    fmt = f"{{:{longest}}}"
    return fmt, "-" * longest


def calc_fraction(n_slides, n_ex, n_words, slug=None):
    if slug in SHORT_CHAPTERS:
        entries = ((n_slides, SLIDES_PER / 2), (n_words, WORDS_PER / 2))
    else:
        entries = (
            (n_slides, SLIDES_PER),
            (n_ex, EXERCISES_PER),
            (n_words, WORDS_PER),
        )
    frac = sum(entry[0] / entry[1] for entry in entries)
    return int(100 * frac / len(entries))


def choose_wrapper(options):
    """Choose how to wrap status figures."""
    if options.colorize:
        return colorize
    if options.markdown:
        return markdownify
    return lambda x: f"{x}%"


def colorize(fraction):
    if fraction < THRESHOLD_LOW:
        return f"{util.RED}{fraction}%{util.ENDC}"
    elif fraction > THRESHOLD_HIGH:
        return f"{util.BLUE}{fraction}%{util.ENDC}"
    else:
        return f"{util.GREEN}{fraction}%{util.ENDC}"


def count_page(slug):
    with open(Path("src", slug, "index.md"), "r") as reader:
        page = reader.read()
        return (
            count_re(regex.EXERCISE_HEADER, page),
            count_re(regex.FIGURE, page),
            count_words(page),
        )


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
    tbl.field_names = "Chapter Slides Exercises Figures Words Overall".split()
    tbl.align = "r"
    tbl.align["Chapter"] = "l"
    return tbl


def markdownify(fraction):
    if fraction < 80:
        return f"**{fraction}%**"
    elif fraction > 120:
        return f"*{fraction}%*"
    else:
        return f"{fraction}%"


def overall(chapters, n_slides, n_ex, n_words):
    n_chapters = (len(chapters) - len(SHORT_CHAPTERS)) + (len(SHORT_CHAPTERS) / 2)
    frac = calc_fraction(n_slides, n_ex, n_words)
    return int(frac / n_chapters)


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--colorize", default=False, action="store_true", help="Colorize text"
    )
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument(
        "--markdown", default=False, action="store_true", help="Bold/italic text"
    )
    return parser.parse_args()


def report(wrapper, chapters):
    """Status of chapters."""
    tbl = make_table()
    tot_slides, tot_ex, tot_fig, tot_words = 0, 0, 0, 0
    for slug in chapters.keys():
        n_ex, n_fig, n_words = count_page(slug)
        n_slides = count_slides(slug)
        tot_ex += n_ex
        tot_fig += n_fig
        tot_slides += n_slides
        tot_words += n_words
        frac = calc_fraction(n_slides, n_ex, n_words, slug)
        frac = wrapper(frac)
        tbl.add_row([slug, n_slides, n_ex, n_fig, n_words, f"{frac}"])
    tbl.add_row(
        [
            "Total",
            tot_slides,
            tot_ex,
            tot_fig,
            tot_words,
            f"{overall(chapters, tot_slides, tot_ex, tot_words)}%",
        ]
    )
    tbl.add_row(
        [
            "Average",
            f"{(tot_slides / len(chapters)):.1f}",
            f"{(tot_ex / len(chapters)):.1f}",
            f"{(tot_fig / len(chapters)):.1f}",
            f"{tot_words // len(chapters)}",
            "",
        ]
    )
    print(tbl)


if __name__ == "__main__":
    main()
