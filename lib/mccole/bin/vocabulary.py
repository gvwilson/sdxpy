"""Produce or check consolidated vocabulary."""

import argparse
from markdown import markdown
from pathlib import Path
import re
import string
import sys
from bs4 import BeautifulSoup
import util


# Words with punctuation.
SPECIAL = {
    "e.g.",
    "i.e.",
}

# Things to strip.
HEADING = re.compile(r"Section\s+([A-Z]|\d+)(\.\d+)*")
MATH = re.compile(r"\\\(.+?\\\)")
NUMBER = re.compile(r"^(#|0x)?[\d\.–\+]+$")
POSSESSIVE = re.compile("’s")
PUNC_CHARS = r"[\[\]‘’,\.!\?\(\):“”…;%°]*"
PUNC_START = re.compile(r"^" + PUNC_CHARS)
PUNC_END = re.compile(PUNC_CHARS + r"$")
SPACIFY = re.compile(r"[——\(\)]")

# Contractions.
CONTRACTIONS = {
    "Ain’t": "Is not",
    "Didn’t": "Did not",
    "Don’t": "Do not",
    "I’m": "I am",
    "They’re": "They are",
    "We’d": "We would",
    "We’ll": "We will",
    "We’re": "We are",
    "We’ve": "We have",
    "aren’t": "are not",
    "can’t": "can not",
    "couldn’t": "could not",
    "didn’t": "did not",
    "doesn’t": "does not",
    "don’t": "do not",
    "hadn’t": "had not",
    "hasn’t": "has not",
    "haven’t": "have not",
    "isn’t": "is not",
    "or’d": "or",
    "shouldn’t": "should not",
    "they’ll": "they will",
    "they’re": "they are",
    "wasn’t": "was not",
    "weren’t": "were not",
    "we’d": "we would",
    "we’ll": "we will",
    "we’re": "we are",
    "we’ve": "we have",
    "won’t": "will not",
    "wouldn’t": "would not",
    "you’ll": "you will",
    "you’re": "you are",
}

def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    docs = read_docs(options, config)
    words = extract_words(docs)
    display(words)


def display(words):
    """Show words found."""
    for word in sorted(words):
        print(word)


def extract_words(docs):
    """Extract set of all words from documents."""
    words = set()
    for doc in docs:
        text = doc.text
        for (pat, subst) in ((MATH, ""), (HEADING, ""), (SPACIFY, " ")):
            text = pat.sub(subst, text)
        for (original, replacement) in CONTRACTIONS.items():
            text = text.replace(original, replacement)
        for word in text.split():
            words.add(normalize(word))
    return words


def whoops(before, after):
    before = before.split("\n")
    after = after.split("\n")
    if before == after:
        return
    for i in range(len(before)):
        if before[i] != after[i]:
            print(before[i], "!=", after[i])
            return


def normalize(word):
    """Create normalized form of word."""
    original = word
    if word in SPECIAL:
        return word
    if word[0] not in string.ascii_letters:
        return ""
    if ':' in word:
        return ""
    word = PUNC_START.sub("", word)
    word = PUNC_END.sub("", word)
    word = NUMBER.sub("", word)
    word = POSSESSIVE.sub("", word)
    return word


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--slides", default=False, action="store_true", help="Process slides")
    return parser.parse_args()


def read_docs(options, config):
    """Read all HTML documents."""
    result = [_read_doc(Path(config.out_dir, "index.html"), "main")]
    for slug in [*config.chapters, *config.appendices]:
        result.append(_read_doc(Path(config.out_dir, slug, "index.html"), "main"))
    if options.slides:
        for slug in config.chapters:
            result.append(_read_doc(Path(config.out_dir, slug, "slides", "index.html"), "body"))
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
