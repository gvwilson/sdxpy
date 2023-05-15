from stage import Stage

class Read(Stage):
    INPUTS = set()

    def __init__(self, filename):
        super().__init__("source")
        self._filename = filename

    def _run(self):
        with open(self._filename, "r") as reader:
            return [s.rstrip("\n") for s in reader.readlines()]
