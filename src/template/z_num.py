"""Insert a constant."""

def open(expander, node):
    expander.showTag(node, False)
    expander.output(node.attrs["z-num"])

def close(expander, node):
    expander.showTag(node, True)
