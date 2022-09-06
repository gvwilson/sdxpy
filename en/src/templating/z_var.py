class z_var:
    @staticmethod
    def open(expander, node):
        expander.showTag(node, False)
        expander.output(expander.env.find(node.attrs["z-var"]))

    @staticmethod
    def close(expander, node):
        expander.showTag(node, True)
