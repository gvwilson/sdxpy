import re

# Match JavaScript ESLint directives.
ESLINT_FULL_LINE = re.compile(r"^\s*//\s*eslint-")
ESLINT_TRAILING = re.compile(r"\s*//\s*eslint-.+$")

# Match Python Flake8 directives.
FLAKE8_FULL_LINE = re.compile(r"^\s*#\s*noqa")
FLAKE8_TRAILING = re.compile(r"\s*#\s*noqa.+$")

# Internal cross-reference in body of glossary definition.
GLOSSARY_INTERNAL_REF = re.compile(r"\]\(#(.+?)\)")

# Match a reference to a footer link or a URL ref in an index entry.
MARKDOWN_FOOTER_LINK = re.compile(r"\[.*?\]\[(.+?)\]", re.MULTILINE)
INDEX_URL_REF = re.compile(r'\[%\s*i\s+("[^"]+")(\s+("[^"]+"))?(\s+url=("[^"]+"))?\s*%\]')

# Match a Markdown heading with optional attributes.
MARKDOWN_HEADING = re.compile(r"^(#+)\s*(.+?)(\{:\s*#(.+\b)\})?$", re.MULTILINE)

# Match multiple whitespace characters.
MULTISPACE = re.compile(r"\s+", re.DOTALL)

# Match table elements.
TABLE_START = re.compile(r'<div\s+class="table(\s+[^"]+)?"[^>]*?>')
TABLE_CAPTION = re.compile(r'caption="(.+?)"')
TABLE_ID = re.compile(r'id="(.+?)"')
TABLE_FULL = re.compile(
    r'<div\s+caption="(.+?)"\s+class="(table(\s+[^"]+)?)"\s+id="(.+?)">\s*<table>',
    re.DOTALL,
)
