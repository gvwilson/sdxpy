import sys

import regex

PATTERNS = [
    regex.FONT_FAMILY_1,
    regex.FONT_FAMILY_2,
]

for filename in sys.argv[1:]:
    text = open(filename, "r").read()
    fonts = set()
    for pat in PATTERNS:
        fonts |= {m.group(1) for m in pat.finditer(text)}
    if fonts and (fonts != {"Verdana"}):
        print(f"{filename}: {', '.join(sorted(fonts))}")
