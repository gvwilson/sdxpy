"""Produce or check consolidated vocabulary."""

import argparse
import re
from pathlib import Path

import util
from bs4 import BeautifulSoup
from markdown import markdown
from spellchecker import SpellChecker

SUB_DOC = [
    (re.compile(r"\\\(.+?\\\)", re.MULTILINE), ""),
    (re.compile(r"[“”]", re.MULTILINE), ""),
    (re.compile(r"[–…—]"), " "),
]
SUB_WORD = [
    (re.compile(r"^e\.g\.$"), ""),  # e.g.
    (re.compile(r"^i\.e\.$"), ""),  # e.g.
    (re.compile(r"^vs\.$"), ""),  # e.g.
    (re.compile(r"^etc\.$"), ""),  # e.g.
    (re.compile(r"^[‘’]+"), ""),  # angled quotes
    (
        re.compile(r"^\((.*[^\)])$"),
        lambda m: m.group(1),
    ),  # open with paren but no closing paren
    (
        re.compile(r"^([^\(].*)\)$"),
        lambda m: m.group(1),
    ),  # close with paren but no opening paren
    (re.compile(r"^\("), ""),  # leading punctuation
    (re.compile(r"[\?\!\.’,:;%°\)]+$"), ""),  # trailing punctuation
    (re.compile(r"’"), "'"),  # internal angled quote
    (re.compile(r"'s$"), ""),  # possessive
    (re.compile(r"^[\+\#\(\)\d\./-]+$"), ""),  # number-ish things
    (re.compile(r"^doi:.+?$"), ""),  # DOIs
    (re.compile(r"^0x.+$"), ""),  # hex numbers
]


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    extra_words = get_extra_words(options)
    docs = read_docs(options, config)
    words = extract_words(docs)
    checker = SpellChecker()
    unknown = checker.unknown(words) - extra_words
    for word in sorted(unknown):
        print(word)


def extract_words(pages):
    """Extract set of all words from documents."""
    words = set()
    for text in pages:
        text = normalize(text, SUB_DOC)
        words |= {normalize(w, SUB_WORD) for w in text.split()}
    return words


def get_extra_words(options):
    """Load list of extra known words."""
    if not options.extra:
        return set()
    with open(options.extra, "r") as reader:
        return {word.strip() for word in reader.readlines()}


def normalize(text, patterns):
    """Create normalized form of text."""
    for pat, sub in patterns:
        text = pat.sub(sub, text)
    return text


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument(
        "--extra", required=False, help="File containing list of extra known words"
    )
    parser.add_argument(
        "--only", nargs="+", default=[], help="Slugs of pages to process"
    )
    parser.add_argument(
        "--slides", default=False, action="store_true", help="Process slides"
    )
    return parser.parse_args()


def read_docs(options, config):
    """Read all HTML documents."""
    slugs = (
        set(options.only)
        if options.only
        else set([*config.chapters, *config.appendices])
    )
    result = [read_html_file(Path(config.out_dir, "index.html"), "main")]
    for slug in slugs:
        result.append(read_html_file(Path(config.out_dir, slug, "index.html"), "main"))
    if options.slides:
        for slug in config.chapters:
            if slug not in slugs:
                continue
            result.append(
                read_html_file(
                    Path(config.out_dir, slug, "slides", "index.html"), "body"
                )
            )
    return result


def read_html_file(filename, root):
    """Read a single HTML document and extract root element."""
    with open(filename, "r") as reader:
        text = reader.read()
        text = text.replace("<br>", " ").replace("<br/>", " ")  # for glossary
        text = markdown(text, extensions=["md_in_html"])
        doc = BeautifulSoup(text, "html.parser")
        doc = doc.find(root)
        doc = util.cleanup_html(doc, bib=True)
        return doc.text


if __name__ == "__main__":
    main()
