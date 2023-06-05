"""Regenerate GitHub root pages."""

import argparse
import re
import sys
import utils


CONTINUE = re.compile(r"^\{:\s+.continue\}\s*$", re.MULTILINE)
HEADING = re.compile(r"^##\s+(.+?)\s+\{:.+?\}\s+$", re.MULTILINE)
LINK = re.compile(r'\[.+?\]\[(.+?)\]', re.MULTILINE)


def main():
    """Main driver."""
    options = parse_args()

    text = sys.stdin.read()
    text = HEADING.sub(lambda m: f"## {m.group(1)}\n", text)
    text = CONTINUE.sub("", text)

    links = utils.read_yaml(options.links)
    links = {ln["key"]: ln["url"] for ln in links}

    needed = {m.group(1) for m in LINK.finditer(text)}
    needed = {key: links[key] for key in needed if key in links}

    print(f"# {options.title}\n")
    print(text)
    for (key, url) in needed.items():
        print(f"[{key}]: {url}")


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--links", required=True, help="Links file")
    parser.add_argument("--title", required=True, help="Page title")
    return parser.parse_args()


if __name__ == "__main__":
    main()
