"""Show all index terms."""

import argparse
import sys
from pathlib import Path

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
    glossary = {
        entry["key"]: entry[config.lang]["term"]
        for entry in util.read_yaml(config.glossary)
    }
    forward = {slug: get_index(glossary, text) for (slug, text) in prose.items()}
    for key, found in sorted(reverse_dict(forward).items()):
        formatted, problem = render(key, found)
        if (not options.problems) or problem:
            print(formatted)


def get_index(glossary, text):
    """Create set of all index keys in text."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_index_keys, "i")
    parser.register(_glossary_keys, "g")
    temp = {"keys": set(), "glossary": glossary}
    try:
        parser.parse(text, temp)
        return temp["keys"]
    except shortcodes.ShortcodeSyntaxError as exc:
        print(f"%i shortcode parsing error: {exc}", file=sys.stderr)
        sys.exit(1)


def _glossary_keys(pargs, kwargs, extra):
    """Get keys out of glossary entry."""
    extra["keys"].add((extra["glossary"][pargs[0]], True))


def _index_keys(pargs, kwargs, extra):
    """Get keys out of index entry."""
    extra["keys"].add((pargs[0], False))


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--problems", action="store_true", default=False, help="Only show problems")
    return parser.parse_args()


def render(key, found):
    """Add color highlighting."""
    problem = False
    if not any(f.startswith("+") for f in found):
        pass
    elif not found[0].startswith("+"):
        problem = True
        key = f"{util.CHAR_RED}{key}{util.CHAR_END}"
    found = [f"{util.CHAR_BLUE}{f}{util.CHAR_END}" if f.startswith("+") else f for f in found]
    return f"{key}: {', '.join(found)}", problem


def reverse_dict(original):
    """Reverse a dictionary."""
    result = {}
    for slug, value_pairs in original.items():
        for value, in_glossary in value_pairs:
            if value not in result:
                result[value] = []
            formatted = f"+{slug}" if in_glossary else slug
            result[value].append(formatted)
    return result


if __name__ == "__main__":
    main()
