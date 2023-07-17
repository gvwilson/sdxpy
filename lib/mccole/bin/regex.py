import re

# Match font family declaration in SVG.
FONT_FAMILY_1 = re.compile(r";fontFamily=([^;]+);")
FONT_FAMILY_2 = re.compile(r";\s*font-family:\s*([^;]+)\s*;")

# Match code inclusion.
INCLUSION = re.compile(r"(\[%\s+inc.+?%\])")
INCLUSION_FILE = re.compile(r'\[%\s*inc\b.+?(file|html)="(.+?)".+?%\]')
INCLUSION_PAT = re.compile(r'\[%\s*inc\b.+?pat="(.+?)"\s+fill="(.+?)".+?%\]')

# Other markup elements.
BIBLIOGRAPHY_REF = re.compile(r"\[%\s*b\s+(.+?)\s*%\]")
FIGURE = re.compile(r'\[%\s*figure\b.+?slug="(.+?)".+?img="(.+?)".+?%\]', re.DOTALL)
GITHUB_ISSUE = re.compile(r"\[%\s*issue\b\s+(\d+)\s*%\]")
GLOSSARY_REF = re.compile(r'\[%\s*g\s+\b(.+?)\b\s+"(.+?)"\s*%\]')
GLOSSARY_CROSSREF = re.compile(r"\[.+?\]\(\#(.+?)\)", re.DOTALL)
IMAGE = re.compile(r'\[%\s*image\s+src="(.+?)".+?%\]')
INDEX_REF = re.compile(r'\[%\s*i\s+("[^"]+")(\s+("[^"]+"))?(\s+url=("[^"]+"))?\s*%\]')
INDEX_URL = re.compile(r'\[%\s*i\b.+?url="(.+?)"\s*%\]')
SHORTCODE = re.compile(r"\[%.+?%\]")

# Markdown elements.
MARKDOWN_CODE_BLOCK = re.compile("```.+?```", re.DOTALL)
MARKDOWN_CODE_INLINE = re.compile("`.+?`")
MARKDOWN_H2 = re.compile(r"^##\s+(.+?)\s+\{:(.+?)\}\s+$", re.MULTILINE)
MARKDOWN_H3 = re.compile(r"^###\s+(.+?)(\s+\{:(.+?)\}\s+)?$", re.MULTILINE)
MARKDOWN_FOOTER_LINK = re.compile(r"\[.*?\]\[(.+?)\]", re.MULTILINE)
SLIDES_H2 = re.compile(r"^##\s+", re.MULTILINE)

# Styling.
PARAGRAPH_CONTINUE = re.compile(r"^\{:\s+.continue\}\s*$", re.MULTILINE)
EXERCISE_HEADER = re.compile(r"\{:\s+\.exercise\}")
