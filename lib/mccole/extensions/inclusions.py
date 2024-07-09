"""Manage file inclusions."""

from ast import AsyncFunctionDef, ClassDef, FunctionDef, parse, unparse
from pathlib import Path
import textwrap

import ark
import shortcodes

import util


COMMENT = {
    "js": "//",
    "py": "#",
    "sql": "--",
}


class Match:
    """Represent a single match by kind and name."""

    def __init__(self, cls, name):
        """Construct with one or several classes and a name."""
        self._cls = cls
        self._name = name

    def match(self, node):
        """Return node if a match or None if no match."""
        if isinstance(node, self._cls) and (node.name == self._name):
            return node
        return None


@shortcodes.register("inc")
@util.timing
def inclusion(pargs, kwargs, node):
    """Handle external file inclusion."""
    util.require(
        len(pargs) == 1,
        f"Bad 'inc' shortcode: must have one filename not {pargs}",
    )
    name = pargs[0]
    path = Path(ark.site.config["src_dir"], *node.path)
    if util.is_slide_file(node):
        path = path.parent
    path = path / name
    kind = path.suffix.lstrip(".")
    indent = kwargs.get("indent", False)
    ellipsis = "\n…" if kwargs.get("ellipsis", "False") == "True" else ""
    try:
        if "pattern" in kwargs:
            body = _match(node, path, kwargs["pattern"], indent)
        elif "mark" in kwargs:
            body = _extract(node, path, kwargs["mark"], kwargs.get("omit", None))
        else:
            body = _whole(path)
        body = f"```{kind}\n{body}\n```\n"
        cls = f'class="language-{kind}"'
        return f'<div {cls} title="{name}" markdown="1">\n{body}{ellipsis}</div>'
    except OSError:
        util.fail(f"Unable to read inclusion '{path}' in {node}.")


def _extract(node, filepath, mark, omit):
    """Extract portion of file in comment markers."""
    if isinstance(filepath, str):
        filepath = Path(filepath)
    text = filepath.read_text()
    suffix = filepath.suffix.lstrip(".")
    if suffix not in COMMENT:
        return text
    text = _extract_mark(node, text, suffix, mark)
    if omit:
        text = _extract_omit(node, text, suffix, omit)
    return text


def _extract_mark(node, text, suffix, mark):
    """Extract marked text."""
    comment = COMMENT[suffix]
    before = f"{comment} [{mark}]"
    after = f"{comment} [/{mark}]"
    before_in = before in text
    after_in = after in text
    if before_in and after_in:
        text = text.split(before)[1].split(after)[0]
    elif before_in or after_in:
        util.fail(f"Mis-matched mark '{mark}' in '{node.slug}'")
    else:
        util.warn(f"No mark in {node.slug}: '{mark}'")
    return text


def _extract_omit(node, text, suffix, omit):
    """Delete text to be omitted."""
    comment = COMMENT[suffix]
    before = f"{comment} [{omit}]"
    after = f"{comment} [/{omit}]"
    before_in = before in text
    after_in = after in text
    if before_in and after_in:
        text = text.split(before)[0].rstrip() + "\n" + text.split(after)[1]
    elif before_in or after_in:
        util.fail(f"Mis-matched omit in {node.path}: '{omit}'")
    else:
        util.warn(f"No omit in {node.slug}: '{omit}'")
    return text


def _match(node, filepath, pattern, indent):
    """Match a pattern against the contents of a file."""
    if isinstance(filepath, str):
        filepath = Path(filepath)
    doc = parse(filepath.read_text())
    matchers = _translate_pattern(pattern)
    node = _match_rec(doc, matchers)
    if not node:
        util.warn(f"Failed to match inclusion pattern in {node.path}: '{filepath}' and '{pattern}'")
        return None
    result = unparse(node)
    if indent:
        result = textwrap.indent(result, " " * node.col_offset)
    return result


def _match_rec(node, exprs):
    """Match recursively, returning node or None."""
    first, rest = exprs[0], exprs[1:]
    for stmt in node.body:
        if found := first.match(stmt):
            return _match_rec(found, rest) if rest else found
    return None


def _translate_pattern(pattern):
    """Turn a pattern into a list of matching objects."""

    lookup = {
        "class": ClassDef,
        "func": (AsyncFunctionDef, FunctionDef),
        "meth": (AsyncFunctionDef, FunctionDef),
    }

    def _translate_one(p):
        cls, name = p.split(":")
        return Match(lookup[cls], name)

    return [_translate_one(p) for p in pattern.split()]


def _whole(path):
    """Get an entire file."""
    lines = path.read_text().split("\n")
    return textwrap.dedent("\n".join(x.rstrip() for x in lines))
