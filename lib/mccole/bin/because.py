"""Figure out why one chapter depends on another."""

from pathlib import Path
import sys

import util


def main():
    assert len(sys.argv) == 5
    glossary_file = sys.argv[1]
    lang = sys.argv[2]
    slugs = sys.argv[3:]

    glossary = util.read_glossary(glossary_file)
    glossary = {key: entry[lang]["term"] for (key, entry) in glossary.items()}

    prose = {
        a: open(Path("src", a, "index.md"), "r").read()
        for a in slugs
    }
    terms = util.find_index_terms(prose)
    defined = {
        slug: set(glossary[entry[0]] for entry in words if entry[1])
        for (slug, words) in terms.items()
    }
    used = {
        slug: set(entry[0] for entry in words if not entry[1])
        for (slug, words) in terms.items()
    }
    print(f"{slugs[0]} <- {slugs[1]}: {', '.join(sorted(defined[slugs[0]].intersection(used[slugs[1]])))}")
    print(f"{slugs[0]} -> {slugs[1]}: {', '.join(sorted(defined[slugs[1]].intersection(used[slugs[0]])))}")

if __name__ == "__main__":
    main()
