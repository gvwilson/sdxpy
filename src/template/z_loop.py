"""Repeat operations."""

def open(expander, node):
    index_name, target_name = node.attrs["z-loop"].split(":")
    expander.showTag(node, False)
    target = expander.env.find(target_name)
    for value in target:
        expander.env.push({index_name: value})
        for child in node.children:
            expander.walk(child)
        expander.env.pop()
    return False

def close(expander, node):
    expander.showTag(node, True)
