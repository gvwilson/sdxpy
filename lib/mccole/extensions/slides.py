"""Generate list of slides."""

import ivy
import shortcodes
import util


@ivy.filters.register(ivy.filters.Filter.FILE_TEXT)
def add_markdown_link_list(text, meta_dict):
    """Add all Markdown links to slides for conversion to HTML."""
    if meta_dict.get("template", None) == "slides":
        text += "\n\n" + util.make_links_table()
    return text


@shortcodes.register("slides")
def slide_list(pargs, kwargs, node):
    """Generate list of slides with links."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'slides' shortcode {pargs} and {kwargs}",
    )
    titles = util.get_config("titles")
    result = ["<ol>"]
    for entry in titles["chapters"]:
        if ivy.nodes.node(f"@root/{entry.slug}/slides/"):
            prefix = f'<a href="@root/{entry.slug}/slides/" markdown="1">'
            suffix = "</a>"
        else:
            prefix = ""
            suffix = ""
        result.append(f"<li>{prefix}{entry.title}{suffix}</li>")
    result.append("</ol>")
    return "\n".join(result)
