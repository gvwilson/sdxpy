#!/usr/bin/env python

"""Remove code and math before spell-checking."""


import argparse
import sys
from bs4 import BeautifulSoup, Tag
from markdown import markdown


def main():
    options = parse_args()
    handle(options.pages)
    handle(options.slides, markdown)


def cleanup(soup):
    for tag in ("head", "pre", "code"):
        for node in soup.find_all(tag):
            node.decompose()
    for (tag, cls) in (("div", "code-sample"),):
        for node in soup.find_all(tag, class_=cls):
            node.decompose()
    return soup


def handle(filenames, pre_processor=None):
    for f in filenames:
        with open(f, "r") as reader:
            text = reader.read()
            if pre_processor is not None:
                text = pre_processor(text)
            print(cleanup(BeautifulSoup(text, "html.parser")))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", nargs="+", default=[], help="pages")
    parser.add_argument("--slides", nargs="+", default=[], help="slides")
    return parser.parse_args()


if __name__ == "__main__":
    main()
