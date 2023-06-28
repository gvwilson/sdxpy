#!/usr/bin/env python

"""Create single-page HTML version of book."""

import argparse
import os

from bs4 import BeautifulSoup


def main():
    """Main driver."""
    options = parse_args()

    with open(os.path.join(options.root, "index.html"), "r") as reader:
        soup = BeautifulSoup(reader.read(), "html.parser")
    body = soup.find("body")

    content = open(options.head, "r").read()
    content = fill_template(options, content)
    content += part(options.root, body, "ol.toc-chapter")
    content += part(options.root, body, "ol.toc-appendix")
    content += open(options.foot, "r").read()

    print(content)


def fill_template(options, text):
    """Fill in template values."""
    for key in ["title", "tagline"]:
        text = text.replace(f"${key}$", vars(options)[key])
    return text


def get(path, slug):
    """Get content from page."""
    with open(path, "r") as reader:
        soup = BeautifulSoup(reader.read(), "html.parser")

    main = soup.find("main")
    main.name = "section"
    main["class"] = "new-chapter"
    patch_part_refs(main)
    patch_glossary(main)
    patch_images(main, slug)
    patch_bib_refs(main)

    title = soup.find("h1")
    title["id"] = slug
    title.string = title.text
    main.insert(0, title)

    return str(main)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--head", required=True, help="HTML head")
    parser.add_argument("--foot", required=True, help="HTML foot")
    parser.add_argument("--root", required=True, help="root directory")
    parser.add_argument("--tagline", required=True, help="site tagline")
    parser.add_argument("--title", required=True, help="site title")
    return parser.parse_args()


def part(root, body, key):
    """Construct part of table of contents."""
    toc = body.select_one(key)
    content = []
    for ref in toc.find_all("a"):
        slug = ref.attrs["href"].rstrip("/")
        path = os.path.join(root, slug, "index.html")
        content.append(get(path, slug))
    return "\n".join(content)


def patch_bib_refs(main):
    """Fix bibliography references."""
    b = "../bibliography/"
    for node in main.select("a.bibref"):
        if node.attrs["href"].startswith(b):
            node.attrs["href"] = node.attrs["href"].replace(b, "")


def patch_part_refs(main):
    """Fix chapter/appendix references."""
    for node in main.select("a"):
        if (
            ("href" in node.attrs)
            and node.attrs["href"].startswith("../")
            and (node.attrs["href"].endswith("/"))
        ):
            node.attrs["href"] = node.attrs["href"].replace("../", "#", 1)[:-1]


def patch_glossary(content):
    """Patch glossary references."""
    g = "../glossary/"
    for node in content.select("a.glossref"):
        if node.attrs["href"].startswith(g):
            node.attrs["href"] = node.attrs["href"].replace(g, "")
    for node in content.select("span.glosskey"):
        if "break-before" in node.attrs["class"]:
            node.attrs["class"] = [
                c for c in node.attrs["class"] if c != "break-before"
            ]
            if "class" in node.parent.attrs:
                node.parent.attrs["class"].append("break-before")
            else:
                node.parent.attrs["class"] = ["break-before"]


def patch_images(content, slug):
    """Patch image references."""
    for node in content.find_all("img"):
        if node.attrs["src"].startswith("./"):
            relative = node.attrs["src"][2:]
            node.attrs["src"] = f"./{slug}/{relative}"


if __name__ == "__main__":
    main()
