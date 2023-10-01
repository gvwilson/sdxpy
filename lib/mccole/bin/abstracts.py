"""Show all abstracts."""

import argparse
import frontmatter
from pathlib import Path

import regex
import util


SECTION = """\
## Chapter {number}: {title}

{abstract}
"""


def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    for (i, (slug, title)) in enumerate(config.chapters.items()):
        with open(Path("src", slug, "index.md"), "r") as reader:
            page = reader.read()
            abstract = frontmatter.loads(page).get("abstract", "No abstract")
            abstract = regex.MULTISPACE.sub(" ", abstract).rstrip()
            print(SECTION.format(number=i+1, title=title, abstract=abstract))


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
