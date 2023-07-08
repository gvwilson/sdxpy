"""Produce or check consolidated vocabulary."""

import argparse
import re
import string
import sys
from pathlib import Path

import util
from bs4 import BeautifulSoup
from markdown import markdown
from spellchecker import SpellChecker

PAT_DOC = [
    (re.compile(r"\\\(.+?\\\)"), " "),  # math
    (re.compile(r"[–—/]"), " "),  # em-dash, en-dash, and slash
    (re.compile(r"e\.g\.", re.IGNORECASE), " "),  # special words
    (re.compile(r"i\.e\.", re.IGNORECASE), " "),
    (re.compile(r"vs\.", re.IGNORECASE), " "),
    (re.compile(r"\(ab\)"), " "),  # (ab)using
    (re.compile(r"\(s\)"), " "),  # file(s)
]
PAT_WORD = [
    (re.compile(r"^[“”’‘…\(\)#]*"), ""),  # leading punctuation
    (re.compile(r"[“”’‘…,\?!\.:;\(\)°%]*$"), ""),  # trailing punctuation
    (re.compile(r"’s"), ""),  # possessive
    (re.compile(r"^(0x)?[e\d\.×\+/–-]+$"), ""),  # number-ish things
    (re.compile(r"^doi:.+"), ""),  # DOIs
    (re.compile(r"’"), "'"),  # normalize apostrophe
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


def extract_words(docs):
    """Extract set of all words from documents."""
    words = set()
    for doc in docs:
        text = normalize(doc.text, PAT_DOC)
        words |= {normalize(w, PAT_WORD) for w in text.split()}
    return words


def get_extra_words(options):
    """Load list of extra known words."""
    if not options.extra:
        return set()
    with open(options.extra, "r") as reader:
        return {word.strip() for word in reader.readlines()}


def normalize(text, patterns):
    """Create normalized form of text."""
    for pat, replacement in patterns:
        text = pat.sub(replacement, text)
    return text


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--extra", help="File containing list of extra known words")
    parser.add_argument(
        "--slides", default=False, action="store_true", help="Process slides"
    )
    return parser.parse_args()


def read_docs(options, config):
    """Read all HTML documents."""
    result = [_read_doc(Path(config.out_dir, "index.html"), "main")]
    for slug in [*config.chapters, *config.appendices]:
        result.append(_read_doc(Path(config.out_dir, slug, "index.html"), "main"))
    if options.slides:
        for slug in config.chapters:
            result.append(
                _read_doc(Path(config.out_dir, slug, "slides", "index.html"), "body")
            )
    return result


def _read_doc(filename, root):
    """Read a single HTML document."""
    with open(filename, "r") as reader:
        text = reader.read()
        text = markdown(text, extensions=["md_in_html"])
        soup = BeautifulSoup(text, "html.parser").find(root)
        return util.cleanup_html(soup, bib=True)


if __name__ == "__main__":
    main()
