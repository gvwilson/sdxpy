"""Create links table."""

from pathlib import Path

import ivy
import shortcodes
import yaml
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

import util


@ivy.events.register(ivy.events.Event.INIT)
def links_append():
    """Add Markdown links table to Markdown files."""
    if "links" not in ivy.site.config:
        return

    links = _read_links()
    links = "\n".join([f"[{x['key']}]: {x['url']}" for x in links])

    def visitor(node):
        if node.ext == "md":
            node.text += "\n\n" + links

    ivy.nodes.root().walk(visitor)


@shortcodes.register("links")
def links_table(pargs, kwargs, node):
    """Create a table of links."""
    util.require("links" in ivy.site.config, "No links specified")

    lang = ivy.site.config.get("lang", None)
    util.require(lang is not None, "No language specified")

    links = _read_links()
    links.sort(key=lambda x: _link_key(x, lang))
    cls = 'class="link-ref"'
    links = "\n".join(
        f'<li>{x[lang]}: <a {cls} href="{x["url"]}">{x["url"]}</a></li>'
        for x in links
    )
    return f"<ul>\n{links}\n</ul>"


@ivy.events.register(ivy.events.Event.EXIT)
def check():
    """Check link usage."""
    used = set()
    ext = LinkCollectorExtension(used)
    ivy.nodes.root().walk(
        lambda node: util.markdownify(node.text, ext=ext, strip=False)
    )

    defined = {d["url"] for d in _read_links()}

    util.warn("unknown links", used - defined)
    util.warn("unused links", defined - used)


class LinkCollectorExtension(Extension):
    def __init__(self, used, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.used = used

    def extendMarkdown(self, md):
        coll = LinkCollector(md, self.used)
        md.treeprocessors.register(coll, "linkcollector", 15)


class LinkCollector(Treeprocessor):
    def __init__(self, md, used):
        super().__init__(md)
        self.used = used

    def run(self, root):
        for element in root.iter("a"):
            self.used.add(element.attrib["href"])
        return root


def _link_key(item, lang):
    """Create sorting key for link."""
    key = item[lang].lower()
    if key.startswith("a "):
        key = key[2:]
    elif key.startswith("the "):
        key = key[4:]
    return key.strip()


def _read_links():
    """Read links file."""
    filepath = Path(ivy.site.home(), ivy.site.config["links"])
    with open(filepath, "r") as reader:
        return yaml.safe_load(reader)
