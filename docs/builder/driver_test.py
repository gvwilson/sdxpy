class NotReallyABuilder:
    def __init__(self, args):
        self.args = args

    def build(self):
        print(f"Building with {self.args}")


def make_builder(args):
    return NotReallyABuilder(args)
