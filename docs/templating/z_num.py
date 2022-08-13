class z_num:
    @staticmethod
    def open(expander, node):
        expander.showTag(node, False)
        expander.output(node.attrs["z-num"])

    @staticmethod
    def close(expander, node):
        expander.showTag(node, True)
