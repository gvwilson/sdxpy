import re

# Match font family declaration in SVG.
FONT_FAMILY_1 = re.compile(r";fontFamily=([^;]+);")
FONT_FAMILY_2 = re.compile(r";\s*font-family:\s*([^;]+)\s*;")

# Match code inclusion.
INCLUSION = re.compile(r"(\[%\s+inc.+?%\])")
INCLUSION_FILE = re.compile(r'\[%\s*inc\b.+?(file|html)="(.+?)".+?%\]')
INCLUSION_PAT = re.compile(r'\[%\s*inc\b.+?pat="(.+?)"\s+fill="(.+?)".+?%\]')

# Other markup elements.
FIGURE = re.compile(r'\[%\s*figure\b.+?slug="(.+?)".+?img="(.+?)".+?%\]', re.DOTALL)
GLOSSARY_REF = re.compile(r'\[%\s*g\s+\b(.+?)\b\s+"(.+?)"\s*%\]')
GLOSSARY_CROSSREF = re.compile(r"\[.+?\]\(\#(.+?)\)", re.DOTALL)
IMG = re.compile(r'<img.+?src="(.+?)".+?>')
SHORTCODE = re.compile(r"\[%.+?%\]")

# Markdown elements.
MARKDOWN_CODE_BLOCK = re.compile("```.+?```", re.DOTALL)
MARKDOWN_CODE_INLINE = re.compile("`.+?`")
MARKDOWN_HEADING = re.compile(r"^##\s+(.+?)\s+\{:(.+?)\}\s+$", re.MULTILINE)
MARKDOWN_FOOTER_LINK = re.compile(r"\[.*?\]\[(.+?)\]", re.MULTILINE)

# Styling.
PARAGRAPH_CONTINUE = re.compile(r"^\{:\s+.continue\}\s*$", re.MULTILINE)
EXERCISE_HEADER = re.compile(r"\{:\s+\.exercise\}")
