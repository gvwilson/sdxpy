import ark
import shortcodes
import util

HEADING = """<p class="continue">
<a href="@root/{slug}" markdown="1" class="syllabus-backref">{title}</a>
<span class="notex">(<a href="@root/{slug}/slides.html">slides</a>)</span>
</p>
"""

@shortcodes.register("syllabus")
@util.timing
def syllabus(pargs, kwargs, node):
    """Display syllabus."""
    metadata = ark.site.config["_meta_"]
    result = []
    for slug in ark.site.config["chapters"]:
        util.require(slug in metadata, f"no metadata for {slug}")
        if "syllabus" not in metadata[slug]:
            continue
        result.append(HEADING.format(slug=slug, title=metadata[slug]["title"]))
        result.append("<ul>")
        for item in metadata[slug]["syllabus"]:
            result.append(f'<li>{util.markdownify(item)}</li>')
        result.append("</ul>")
    return "\n".join(result)
