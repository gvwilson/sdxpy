from stage import Stage

class Cat(Stage):
    INPUTS = {"first", "second"}

    def _run(self):
        return self._available["first"] + self._available["second"]
