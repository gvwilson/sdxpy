from stage import Stage

class Tail(Stage):
    INPUTS = {"input"}

    def __init__(self, num):
        super().__init__()
        self._num = num

    def _run(self):
        data = self._available["input"]
        return data[-self._num:]
