"""Include files from root directory."""

import re
from pathlib import Path

import ivy
import shortcodes
import util

TITLE = re.compile(r"^#\s+.+?\n")


@shortcodes.register("root")
def root(pargs, kwargs, node):
    """Include a file from the root directory, stripping off its h1 title."""
    util.require((len(pargs) == 1) and not kwargs, "Bad 'root' shortcode")
    filename = pargs[0]
    fullpath = Path(ivy.site.home(), filename)
    util.require(fullpath.exists(), f"No file {filename} in root directory")
    with open(fullpath, "r") as reader:
        content = reader.read()
    content = TITLE.sub("", content)
    return content
