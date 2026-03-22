class Visitor:
    def __init__(self, root):
        self.root = root

    def walk(self, node=None):
        if node is None:
            node = self.root
        if self.open(node):
            for child in node.children:
                self.walk(child)
        self.close(node)

    def open(self, node):
        raise NotImplementedError("open")

    def close(self, node):
        raise NotImplementedError("close")
