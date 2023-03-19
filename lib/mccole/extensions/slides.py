"""Generate list of slides."""

import ivy
import shortcodes
import util

_markdown_links = None


@ivy.filters.register(ivy.filters.Filter.FILE_TEXT)
def add_markdown_list(text, meta_dict):
    if meta_dict.get("template", None) == "slides":
        text += "\n\n" + util.make_links_table()
    return text


@shortcodes.register("slides")
def slide_list(pargs, kwargs, node):
    """Convert generate list of slides."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'slides' shortcode {pargs} and {kwargs}",
    )
    titles = util.get_config("titles")
    result = ["<ol>"]
    for entry in titles["chapters"]:
        result.append(
            f'<li><a href="@root/{entry.slug}/slides/" markdown="1">{entry.title}</a></li>'
        )
    result.append("</ol>")
    return "\n".join(result)
