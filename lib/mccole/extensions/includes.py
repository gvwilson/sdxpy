"""Handle file inclusions

The `[% inc ... %]` shortcode includes other files or portions of
other files:

-   `[% inc file="path" %]` includes an entire file. The path is
    relative to the including file.

-   `[% inc file="path" keep="key" %]` includes everything between
    lines marked with `[key]` and `[/key]`.  (These markers are usually
    placed in comments.)

-   `[% inc file="path" omit="key" %]` omits everything between
    markers.

-   `[% inc file="path" keep="outer" omit="inner" %]` selects the
    lines within the `outer` section, then omits lines within that
    section marked with `inner`.

-   `[% inc pat="path.*" fill="one two" %]` includes the files
    `path.one` and `path.two` (i.e., replaces `*` in `pat` with each
    of the tokens in `fill`, then includes all of that file).

To make this work:

-   `filter_files` tells Ivy to only process files ending in `.html`
    and `.md` so that it won't try to templatize source code files.

-   `copy_files` copies all of the files used as inclusions to the
    output directory so that they can be linked to. It assumes that
    a chapter or appendix `A` generates `docs/A/index.html` so that
    the included file can be copied to `docs/A/whatever`.

-   `include` handles file inclusion.  If the `node` argument is
    empty, it's too early in the processing cycle, so the function
    does nothing; otehrwise, it dispatches to a case-specific handler.
"""

import re
from pathlib import Path

import ivy
import shortcodes
import util


@ivy.filters.register(ivy.filters.Filter.LOAD_NODE_FILE)
def filter_files(value, filepath):
    """Only process HTML and Markdown files."""
    result = filepath.suffix in {".html", ".md"}
    return result


@shortcodes.register("linecount")
def linecount(pargs, kwargs, node):
    """Count lines in an include file."""
    util.require(
        not kwargs,
        f"Badly-formatted linecount shortcode with {kwargs} in {node.filepath}",
    )

    inclusions = util.make_config("inclusions")
    filepath = _inclusion_filepath(inclusions, node, pargs[0])
    with open(filepath, "r") as reader:
        return str(len(reader.readlines()))


@shortcodes.register("inc")
def include(pargs, kwargs, node):
    """Handle a file inclusion, possibly excerpting."""
    util.require(
        not pargs, f"Badly-formatted excerpt shortcode with {pargs} in {node.filepath}"
    )

    # Handle by cases.
    inclusions = util.make_config("inclusions")
    if ("pat" in kwargs) and ("fill" in kwargs):
        return _multi(inclusions, node, **kwargs)
    elif "file" not in kwargs:
        util.fail(f"Badly-formatted excerpt shortcode with {kwargs} in {node.filepath}")
    elif ("keep" in kwargs) and ("omit" in kwargs):
        return _keep_omit(inclusions, node, **kwargs)
    elif "keep" in kwargs:
        return _keep(inclusions, node, **kwargs)
    elif "omit" in kwargs:
        return _omit(inclusions, node, **kwargs)
    else:
        return _file(inclusions, node, **kwargs)


def _file(inclusions, node, file):
    """Handle a simple file inclusion."""
    filepath = _inclusion_filepath(inclusions, node, file)
    return _include_file(node, filepath)


def _html(inclusions, node, html):
    """Handle an HTML file inclusion."""
    filepath = _inclusion_filepath(inclusions, node, html)
    with open(filepath, "r") as reader:
        content = reader.read().rstrip()
    return f'<div class="html">\n{content}\n</div>'


def _keep(inclusions, node, file, keep):
    """Handle a sliced file inclusion."""
    filepath = _inclusion_filepath(inclusions, node, file)
    return _include_file(node, filepath, lambda lns: _keep_lines(filepath, lns, keep))


def _keep_omit(inclusions, node, file, keep, omit):
    """Handle an inclusion that keeps some content but omits other."""
    filepath = _inclusion_filepath(inclusions, node, file)
    return _include_file(
        node,
        filepath,
        lambda lns: _keep_lines(filepath, lns, keep),
        lambda lns: _omit_lines(filepath, lns, omit),
    )


def _multi(inclusions, node, pat, fill):
    """Handle multiple file inclusion."""
    result = []
    replacements = [r.strip() for r in fill.strip().split()]
    replacements = [r for r in replacements if r]
    for rep in replacements:
        file = pat.replace("*", rep)
        result.append(_file(inclusions, node, file))
    return "\n\n".join(result)


def _omit(inclusions, node, file, omit):
    """Handle an erasing file inclusion."""
    filepath = _inclusion_filepath(inclusions, node, file)
    return _include_file(node, filepath, lambda lns: _omit_lines(filepath, lns, omit))


def _find_markers(lines, key):
    """Find start/stop markers in files."""
    start = f"[{key}]"
    stop = f"[/{key}]"
    i_start = None
    i_stop = None
    for (i, line) in enumerate(lines):
        if start in line:
            i_start = i
        elif stop in line:
            i_stop = i
    return i_start, i_stop


def _include_file(node, filepath, *filters):
    """Include a file, filtering if asked to."""
    kind = filepath.split(".")[-1]
    try:
        with open(filepath, "r") as reader:
            lines = reader.readlines()
            for f in STANDARD_FILTERS:
                lines = f(lines)
            for f in filters:
                lines = f(lines)
            return _make_html(node, Path(filepath).name, kind, lines)
    except OSError:
        util.fail(f"Unable to read inclusion '{filepath}' in {node.filepath}.")


def _is_slides(node):
    """Is this a slides file?"""
    return node.meta.get("template", None) == "slides"


def _keep_lines(filepath, lines, key):
    """Select lines between markers."""
    start, stop = _find_markers(lines, key)
    util.require(
        (start is not None) and (stop is not None),
        f"Failed to match inclusion 'keep' key {key} in {filepath}",
    )
    result = []
    while start is not None:
        result += lines[start + 1 : stop]
        lines = lines[stop:]
        start, stop = _find_markers(lines, key)
    return result


def _make_html(node, name, kind, lines):
    """Construct HTML inclusion from lines."""
    body = "\n".join(x.rstrip() for x in lines)
    body = f"```{kind}\n{body}\n```\n"
    if _is_slides(node):
        return body
    else:
        cls = f'class="code-sample lang-{kind}"'
        md = 'markdown="1"'
        return f'<div {cls} title="{name}" {md}>\n{body}</div>'


def _omit_lines(filepath, lines, key):
    """Remove lines between markers."""
    start, stop = _find_markers(lines, key)
    util.require(
        (start is not None) and (stop is not None),
        f"Failed to match inclusion 'omit' key {key} in {filepath}",
    )
    while start is not None:
        lines = lines[:start] + lines[stop + 1 :]
        start, stop = _find_markers(lines, key)
    return lines


def _inclusion_filepath(inclusions, node, file):
    """Make path to included file."""
    src, dst = util.make_copy_paths(node, file)
    inclusions[src] = dst
    return src


ESLINT_FULL_LINE = re.compile(r"^\s*//\s*eslint-")
ESLINT_TRAILING = re.compile(r"\s*//\s*eslint-.+$")


def _remove_eslint(lines):
    """Remove eslint markers."""
    lines = [ln for ln in lines if not ESLINT_FULL_LINE.match(ln)]
    lines = [ESLINT_TRAILING.sub("", ln) for ln in lines]
    return lines


FLAKE8_FULL_LINE = re.compile(r"^\s*#\s*noqa")
FLAKE8_TRAILING = re.compile(r"\s*#\s*noqa.+$")


def _remove_flake8(lines):
    """Remove flake8 markers."""
    lines = [ln for ln in lines if not FLAKE8_FULL_LINE.match(ln)]
    lines = [FLAKE8_TRAILING.sub("", ln) for ln in lines]
    return lines


STANDARD_FILTERS = [_remove_eslint, _remove_flake8]
