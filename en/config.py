"""Ivy configuration file."""

import os

# Abbreviation for this document.
abbrev = "sdxpy"

# GitHub repository.
repo = "https://github.com/gvwilson/sdpy"

# Site settings.
lang = "en"
title = "Software Design in Python"
acronym = "SDPy"
tagline = "a tool-based introduction"
author = "Greg Wilson"
email = "gvwilson@third-bit.com"
domain = "third-bit.com"
plausible = True
archive = f"{abbrev}-examples.zip"
draft = True

# Chapters.
chapters = [
    "introduction",
    "tester",
    "interpreter",
    "backup",
    "cache",
    "dataframe",
    "persistence",
    "binary",
    "builder",
    "templating",
    "layout",
    "editor",
    "server",
    "packman",
    "matching",
    "parser",
    "linter",
    "vm",
    "debugger",
    "conclusion",
]

# Appendices (slugs in order).
appendices = [
    "bibliography",
    "syllabus",
    "slides",
    "license",
    "conduct",
    "contributing",
    "glossary",
    "credits",
    "contents",
]

# Files to copy verbatim.
copy = [
    "*.ht",
]

# Exclusions (don't process).
exclude = [
    "*.as",
    "*.ht",
    "*.mx",
    "*.tll",
]

# Things to ignore when linting.
unreferenced = [
    "slides/index.html"
]

# Debug.
debug = True

# Warn about missing or unused entries.
warnings = True

# ----------------------------------------------------------------------

# Theme.
theme = "mccole"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "markdown.extensions.smarty",
        "pymdownx.superfences",
    ]
}

# External files.
acknowledgments = "info/acknowledgments.yml"
bibliography = "info/bibliography.bib"
bibliography_style = "unsrt"
credits = "info/credits.yml"
glossary = "info/glossary.yml"
links = "info/links.yml"
dom = "lib/mccole/dom.yml"

# Input and output directories.
src_dir = "src"
out_dir = os.getenv("MCCOLE", "docs")

# Use "a/" URLs instead of "a.html".
extension = "/"

# Files to copy verbatim.
copy += [
    "*.jpg",
    "*.js",
    "*.json",
    "*.out",
    "*.png",
    "*.py",
    "*.sh",
    "*.svg",
    "*.txt",
    "*.yml",
]

# Exclusions (don't process).
exclude += [
    "Makefile",
    "*.csv",
    "*.ht",
    "*.jpg",
    "*.js",
    "*.json",
    "*.mk",
    "*.out",
    "*.pdf",
    "*.png",
    "*.py",
    "*.pyc",
    "*.sh",
    "*.svg",
    "*.txt",
    "*.yml",
    "*~",
    "__pycache__",
    ".pytest_cache",
]

# ----------------------------------------------------------------------

# Display values for LaTeX generation.
if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 2, "Expect exactly one argument"
    if sys.argv[1] == "--abbrev":
        print(abbrev)
    elif sys.argv[1] == "--latex":
        print(f"\\title{{{title}}}")
        print(f"\\subtitle{{{tagline}}}")
        print(f"\\author{{{author}}}")
    elif sys.argv[1] == "--tagline":
        print(tagline)
    elif sys.argv[1] == "--title":
        print(title)
    else:
        assert False, f"Unknown flag {sys.argv[1]}"
