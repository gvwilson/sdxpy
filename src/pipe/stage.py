class Stage:
    def __init__(self):
        self._required = self.INPUTS.copy()
        self._available = {}
        self._result = None
        self._tell = []

    def tell(self, other, key):
        self._tell.append((other, key))

    def ready(self):
        return len(self._required) == 0

    def notify(self, name, value):
        print(f"{self.__class__.__name__} notify({name}, {value})")
        assert name in self._required
        self._available[name] = value
        self._required.remove(name)
        self.run()

    def run(self):
        if self.ready():
            self._result = self._run()
            for (other, key) in self._tell:
                other.notify(key, self._result)

    def result(self):
        assert self.ready()
        return self._result
