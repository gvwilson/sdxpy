"""Ivy configuration file."""

# Get standard settings.
import sys
sys.path.insert(0, "info")
from mccole import *
del sys.path[0]

# Abbreviation for this document.
abbrev = "sdxpy"

# GitHub repository.
repo = "https://github.com/gvwilson/sdpy"

# Site title and subtitle.
lang = "en"
title = "Software Design in Python"
acronym = "SDPy"
tagline = "a tool-based introduction"
author = "Greg Wilson"
email = "gvwilson@third-bit.com"
plausible = "" # "third-bit.com"

# Chapters.
chapters = [
    "introduction",
    "tester",
    "backup",
    "interpreter",
    "dataframe",
    "pipeline",
    "builder",
    "matching",
    "parser",
    "server",
    "cache",
    "database",
    "persistence",
    "binary",
    "templating",
    "packman",
    "layout",
    "linter",
    "codegen",
    "vm",
    "debugger",
    "conclusion",
]

# Appendices (slugs in order).
appendices = [
    "bibliography",
    "syllabus",
    "license",
    "conduct",
    "contributing",
    "glossary",
    "credits",
    "contents",
]

# To do.
todo = []

# Debug.
debug = True

# Warn about missing or unused entries.
warnings = True

# Files to copy verbatim.
copy += [
    "*.ht",
]

# Exclusions (don't process).
exclude += [
    "*.as",
    "*.ht",
    "*.mx",
    "*.tll",
]

# Display values for LaTeX generation.
if __name__ == "__main__":
    main(sys.argv, abbrev, title, tagline, author)
