import ivy
import shortcodes
import util


@ivy.events.register(ivy.events.Event.INIT)
def collect_syllabi():
    """Collect chapter syllabi."""
    info = {}
    ivy.nodes.root().walk(lambda node: _collect(info, node))
    syllabi = [
        (slug, info[slug][0], info[slug][1])
        for slug in ivy.site.config["chapters"]
        if slug in info
    ]
    config = util.mccole()
    config["syllabi"] = syllabi


def _collect(info, node):
    if "syllabus" in node.meta:
        assert "title" in node.meta
        info[node.slug] = (node.meta["title"], node.meta.get("syllabus", []))


@shortcodes.register("syllabus")
def syllabus(pargs, kwargs, node):
    """Display syllabus."""
    config = util.mccole()
    result = ["<ul>"]
    for (slug, title, syllabus) in config["syllabi"]:
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
