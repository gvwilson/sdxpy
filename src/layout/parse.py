import re

from micro_dom import DomBlock, DomCol, DomRow

TEXT_AND_TAG = re.compile(r"^([^<]*)(<[^>]+?>)(.*)$", re.MULTILINE)
TAG_AND_ATTR = re.compile(r"<(\w+)([^>]*)>")
KEY_AND_VALUE = re.compile(r'\s*(\w+)="([^"]*)"\s*/')

def parse_html(text):
    chunks = chunkify(text.strip())
    assert(is_element(chunks[0]), "Must have enclosing outer node")
    node, remainder = make_node(chunks)
    assert len(remainder) == 0, "Cannot have dangling content"
    return node


def chunkify(text):
    raw = []
    while (text):
        matches = TEXT_AND_TAG.search(text)
        if not matches:
            break
        raw.append(matches[1])
        raw.append(matches[2])
        text = matches[3]

    if text:
        raw.append(text)

    return [chunk for chunk in raw if len(chunk) > 0]


def is_element(chunk):
    return chunk and (chunk[0] == "<")


# [skip]
# [makenode]
def make_node(chunks):
    assert len(chunks) > 0, "Cannot make nodes without chunks"

    if not is_element(chunks[0]):
        return [DomBlock(chunks[0]), chunks[1:]]

    node = make_opening(chunks[0])
    closing = f"</{node.tag}>"

    remainder = chunks[1:]
    child = None
    while remainder and (remainder[0] != closing):
        child, remainder = make_node(remainder)
        node.children.append(child)

    assert remainder and (remainder[0] == closing), \
        f"Node with tag {node.tag} not closed"

    return node, remainder[1:]
# [/makenode]

# [makeopening]
def make_opening(chunk):
    outer = TAG_AND_ATTR.search(chunk)
    tag = outer[1]

    attributes = {
        k:v for k,v in KEY_AND_VALUE.finditer(outer[2].strip())
    }

    if tag == "col":
        return DomCol(attributes)
    if tag == "row":
        return DomRow(attributes)
    assert False, f"Unrecognized tag name {tag}"
# [/makeopening]
# [/skip]
