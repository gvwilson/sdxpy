"""Ivy configuration file."""

import os

# Abbreviation for this document.
abbrev = "sd4ds"

# GitHub repository.
repo = "https://github.com/gvwilson/sd4ds"

# Site settings.
lang = "en"
title = "Software Design for Data Scientists"
acronym = "SD4DS"
tagline = "a tool-based introduction"
author = "Greg Wilson"
email = "gvwilson@third-bit.com"
domain = "third-bit.com"
plausible = True
archive = f"{abbrev}-examples.zip"
draft = True

# Website.
website = f"https://{domain}/{abbrev}/"

# Chapters.
chapters = [
    "intro",
    "dup",
    "glob",
    "parse",
    "test",
    "mock",
    "archive",
    "oop",
    "meta",
    "check",
    "interp",
    "func",
    "template",
    "lint",
    "perf",
    "persist",
    "binary",
    "db",
    "build",
    "pipe",
    "pack",
    "server",
    "editor",
    "finale",
]

# Appendices (slugs in order).
appendices = [
    "bib",
    "syllabus",
    "slides",
    "license",
    "conduct",
    "contrib",
    "glossary",
    "credits",
    "contents",
]

# To-do
todo = [
    "dup",
    "test",
    "mock",
    "archive",
    "meta",
    "re",
    "parse",
    "check",
    "interp",
    "template",
    "lint",
    "perf",
    "df",
    "plot",
    "persist",
    "binary",
    "db",
    "build",
    "pipe",
    "cache",
    "pack",
    "server",
    "ssg",
    "finale",
]

# Files to copy verbatim.
copy = [
    "*.xml",
]

# Exclusions (don't process).
exclude = [
    "*.dot",
    "*.xml",
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
    "*.webp",
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
    "*.webp",
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
    elif sys.argv[1] == "--chapters":
        print("\n".join(chapters))
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
