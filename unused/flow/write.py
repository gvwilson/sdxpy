from stage import Stage

class Write(Stage):
    INPUTS = {"input"}

    def __init__(self, filename=None):
        super().__init__("sink")
        self._filename = filename

    def _run(self):
        result = self._available["input"]
        if self._filename is None:
            for line in result:
                print(line)
        else:
            with open(self._filename, "w") as writer:
                for line in result:
                    print(line, file=writer)
