from stage import Stage

class Write(Stage):
    INPUTS = {"input"}

    def __init__(self, filename=None):
        super().__init__("sink")
        self._filename = filename

    def _run(self):
        writer = None if self._filename is None else open(self._filename, "w")
        for line in self._available["input"]:
            print(line, file=writer)
        if writer is not None:
            writer.close()

export = Write
