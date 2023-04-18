"""Conditionalize part of a template."""

def open(expander, node):
    check = expander.env.find(node.attrs["z-if"])
    if check:
        expander.showTag(node, False)
    return check

def close(expander, node):
    if expander.env.find(node.attrs["z-if"]):
        expander.showTag(node, True)
