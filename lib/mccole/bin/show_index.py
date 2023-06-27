"""Show all index terms."""

import argparse
from pathlib import Path
import sys

import shortcodes

import util

def main():
    """Main driver."""
    options = parse_args()
    config = util.load_config(options.config)
    prose = {
        slug: open(Path(config.src_dir, slug, "index.md"), "r").read()
        for slug in [*config.chapters.keys(), *config.appendices.keys()]
    }
    forward = {
        slug: get_index_keys(text) for (slug, text) in prose.items()
    }
    for key, slugs in sorted(reverse_dict(forward).items()):
        print(f"{key}: {', '.join(slugs)}")


def get_index_keys(text):
    """Create set of all index keys in text."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_get_keys, "i", "/i")
    temp = set()
    try:
        parser.parse(text, temp)
        return temp
    except shortcodes.ShortcodeSyntaxError as exc:
        print(f"%i shortcode parsing error in {node.filepath}: {exc}", file=sys.stderr)
        sys.exit(1)


def _get_keys(pargs, kwargs, extra, content):
    """Get keys out of index entry."""
    extra.update(key.strip() for key in pargs)


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    return parser.parse_args()


def reverse_dict(original):
    """Reverse a dictionary."""
    result = {}
    for slug, set_of_values in original.items():
        for value in set_of_values:
            if value not in result:
                result[value] = []
            result[value].append(slug)
    return result


if __name__ == "__main__":
    main()
