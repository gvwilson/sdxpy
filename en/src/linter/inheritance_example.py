class Parent:
    def red(self):
        pass

    def green(self):
        pass


class LeftChild(Parent):
    def green(self):
        pass

    def blue(self):
        pass


class RightChild(Parent):
    def red(self):
        pass

    def blue(self):
        pass


class GrandChild(LeftChild):
    def red(self):
        pass

    def blue(self):
        pass

    def orange(self):
        pass
