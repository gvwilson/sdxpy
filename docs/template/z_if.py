class z_if:
    @staticmethod
    def open(expander, node):
        check = expander.env.find(node.attrs["z-if"])
        if check:
            expander.showTag(node, False)
        return check

    @staticmethod
    def close(expander, node):
        if expander.env.find(node.attrs["z-if"]):
            expander.showTag(node, True)
