"""Generate list of acknowledgments."""

import ivy
import shortcodes
import yaml

import util

EMPTY_ENTRY = "<td></td>"
WIDTH = 3


@shortcodes.register("acknowledgments")
def bibliography(pargs, kwargs, node):
    """Convert acknowledgments to HTML table."""
    util.require(
        (not pargs) and (not kwargs),
        "Bad 'acknowledgments' shortcode"
    )
    if (filename := ivy.site.config.get("acknowledgments", None)) is None:
        return '<p class="warning">No acknowledgments specified.</p>'
    with open(filename, "r") as reader:
        entries = yaml.safe_load(reader)
    entries = [_format_entry(e) for e in entries]
    while (len(entries) % WIDTH) != 0:
        entries.append(EMPTY_ENTRY)
    span = range(0, len(entries), WIDTH)
    rows = "\n".join(
        [_format_row(entries[i:(i + WIDTH)]) for i in span]
    )
    return f'<table class="acknowledgments"><tbody>{rows}\n</tbody></table>\n'


def _format_entry(entry):
    """Convert YAML to HTML."""
    if ("url" not in entry) or (not entry["url"]):
        return f'<td>{entry["name"]}</td>'
    cls = 'class="no-footnote"'
    return f'<td><a {cls} href="{entry["url"]}">{entry["name"]}</a></td>'


def _format_row(entries):
    """Convert set of entries to table row."""
    return f'<tr>{"".join(entries)}</tr>'
