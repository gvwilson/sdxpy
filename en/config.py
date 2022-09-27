"""Ivy configuration file."""

# ----------------------------------------

# Abbreviation for this document.
abbrev = "sdxpy"

# GitHub repository.
repo = "https://github.com/gvwilson/sdpy"

# Site title and subtitle.
title = "Software Design in Python"
acronym = "SDPy"
tagline = "a tool-based introduction"
author = "Greg Wilson"

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
todo = {
    "filecache",
    "database",
    "packman",
    "debugger",
}

# Debug.
debug = True

# Warn about missing or unused entries.
warnings = True

# ----------------------------------------

# Use our own theme.
theme = "mccole"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": ["markdown.extensions.extra", "pymdownx.superfences"]
}

# External files.
acknowledgments = "info/acknowledgments.yml"
bibliography = "info/bibliography.bib"
bibliography_style = "unsrt"
credits = "info/credits.yml"
glossary = "info/glossary.yml"
links = "info/links.yml"
dom = "info/dom.yml"

# Language code.
lang = "en"

# Input and output directories.
src_dir = "src"
out_dir = "docs"

# Use "a/" URLs instead of "a.html".
extension = "/"

# Files to copy verbatim.
copy = [
    "*.ht",
    "*.json",
    "*.out",
    "*.pdf",
    "*.png",
    "*.py",
    "*.svg",
]

# Exclusions (don't process).
exclude = [
    "Makefile",
    "*.as",
    "*.csv",
    "*.gz",
    "*.ht",
    "*.json",
    "*.mk",
    "*.mx",
    "*.out",
    "*.pdf",
    "*.png",
    "*.py",
    "*.pyc",
    "*.sh",
    "*.svg",
    "*.tll",
    "*.txt",
    "*.yml",
    "*~",
    "__pycache__",
    ".pytest_cache",
]

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
