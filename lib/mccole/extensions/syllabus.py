import ivy
import shortcodes
import util

@ivy.events.register(ivy.events.Event.INIT)
def collect():
    """Collect information from pages."""
    major = util.make_major()
    collected = {}
    ivy.nodes.root().walk(lambda node: _collect(node, major, collected))
    _cleanup(collected)


def _collect(node, major, collected):
    """Pull data from a single node."""
    if "syllabus" in node.meta:
        assert "title" in node.meta
        collected[node.slug] = (node.meta["title"], node.meta.get("syllabus", []))

def _cleanup(collected):
    """Clean up collected data."""
    syllabi = [
        (slug, collected[slug][0], collected[slug][1])
        for slug in ivy.site.config["chapters"]
        if slug in collected
    ]
    util.make_config("syllabus", syllabi)

# ----------------------------------------------------------------------

@shortcodes.register("syllabus")
def syllabus(pargs, kwargs, node):
    """Display syllabus."""
    syllabi = util.get_config("syllabus")
    result = ["<ul>"]
    for (slug, title, syllabus) in syllabi:
        result.append(f'<li><a href="@root/{slug}" markdown="1">{title}</a>')
        if syllabus:
            result.append("<ul>")
            for item in syllabus:
                result.append(f'<li markdown="1">{item}</li>')
            result.append("</ul>")
        result.append("</li>")
    result.append("</ul>")
    result = "\n".join(result)
    return result
