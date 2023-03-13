from abc import ABC, abstractmethod


class Visitor(ABC):
    def __init__(self, root):
        self.root = root

    def walk(self, node=None):
        if node is None:
            node = self.root
        if self.open(node):
            for child in node.children:
                self.walk(child)
        self.close(node)

    @abstractmethod
    def open(self, node):
        pass

    @abstractmethod
    def close(self, node):
        pass
