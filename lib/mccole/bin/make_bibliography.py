"""Create HTML version of bibliography."""

import argparse
import pybtex.database
import pybtex.plugin
import sys


# How to format bibliography.
BIB_STYLE = "unsrt"


def main():
    """Main driver."""
    args = parse_args()
    try:
        raw = pybtex.database.parse_file(args.infile)
        style = pybtex.plugin.find_plugin("pybtex.style.formatting", BIB_STYLE)()
        styled_bib = style.format_bibliography(raw)
        html = pybtex.plugin.find_plugin("pybtex.backends", "html")()
        entries = [fmt(entry.key, entry.text.render(html)) for entry in styled_bib]
        html = '<dl class="bibliography">\n\n' + "\n\n".join(entries) + "\n\n</dl>"
        with open(args.outfile, "w") as writer:
            print(html, file=writer)
    except FileNotFoundError:
        fail(f"Unable to read bibliography {args.infile}")
    except pybtex.exceptions.PybtexError:
        fail(f"Unable to parse bibliography {args.infile}")


def fail(msg):
    """Fail unilaterally."""
    print(msg, file=sys.stderr)
    raise AssertionError(msg)


def fmt(key, body):
    """Format individual bibliography entry."""
    return f'<dt id="{key}">{key}</dt>\n<dd>{body}</dd>'


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, required=True, help="input file")
    parser.add_argument("--outfile", type=str, required=True, help="output file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
