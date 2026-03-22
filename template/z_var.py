def open(expander, node):
    expander.showTag(node, False)
    expander.output(expander.env.find(node.attrs["z-var"]))

def close(expander, node):
    expander.showTag(node, True)
