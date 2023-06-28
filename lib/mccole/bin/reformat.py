#!/usr/bin/env python

"""Wrap long lines and do other cleanup for code output."""

import argparse
import os
import sys
import textwrap

# Strip out file protocol.
PROTOCOL = "file://"

# Home directory replacement.
HERE = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# How to show removed lines. (Can't use literal ellipsis '…' because it confuses LaTeX.)
REMOVED = "..."

# Output slice size.
SLICE = 10


def reformat(options):
    """Main driver."""
    lines = [x.rstrip() for x in sys.stdin.read().rstrip().split("\n")]
    selected = select(options, lines)
    wrapped = wrap(options, selected)
    for line in wrapped:
        print(line)


def select(options, lines):
    """Select desired lines vertically."""
    if options.slice:
        return lines[:SLICE] + [REMOVED] + lines[-SLICE:]
    return lines


def wrap(options, lines):
    """Wrap lines."""
    result = []
    for line in lines:
        line = line.replace(PROTOCOL, "").replace(HERE, options.home)
        lines = textwrap.wrap(line, width=options.columns)
        if lines:
            result.extend([f"{ln} \\" for ln in lines[:-1]])
            result.append(lines[-1])
        else:
            result.append("")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--columns", type=int, help="Width of columns")
    parser.add_argument("--home", help="Substitute home directory")
    parser.add_argument("--slice", action="store_true", help="Take slice out of input?")
    options = parser.parse_args()
    reformat(options)
