"""Generate list of slides."""

import shortcodes
import util


@shortcodes.register("slides")
def bibliography(pargs, kwargs, node):
    """Convert bibliography to HTML."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'slides' shortcode {pargs} and {kwargs}",
    )
    titles = util.get_config("titles")
    result = ["<ol>"]
    for entry in titles["chapters"]:
        result.append(f'<li><a href="@root/{entry.slug}/slides/" markdown="1">{entry.title}</a></li>')
    result.append("</ol>")
    return "\n".join(result)
