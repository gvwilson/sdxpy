import re
import sys

import yaml

CLEAN = re.compile(r"(.+)\(.+\)")


def main():
    with open(sys.argv[1], "r") as reader:
        glossary = yaml.load(reader, Loader=yaml.FullLoader)
        terms = {cleanup(entry["en"]["term"]) for entry in glossary}

    text = sys.stdin.read()
    for term in sorted(terms):
        if make_pat(term).search(text):
            print(term)


def cleanup(word):
    m = CLEAN.search(word)
    if m:
        word = m.group(1)
    return word.strip()


def make_pat(text):
    return re.compile(r"\b" + text + r"\b")


if __name__ == "__main__":
    main()
