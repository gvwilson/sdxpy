from oop import LoadOop, SaveOop


class SaveAlias(SaveOop):
    def __init__(self, writer):
        super().__init__(writer)
        self.seen = set()

    # [save]
    def save(self, thing):
        thing_id = id(thing)
        if thing_id in self.seen:
            self._write("alias", thing_id, "")
            return

        self.seen.add(thing_id)
        typename = type(thing).__name__
        method = f"save_{typename}"
        assert hasattr(self, method), \
            f"Unknown object type {typename}"
        getattr(self, method)(thing)
    # [/save]

    def save_bool(self, thing):
        self._write("bool", id(thing), thing)

    def save_float(self, thing):
        self._write("float", id(thing), thing)

    def save_int(self, thing):
        self._write("int", id(thing), thing)

    def save_list(self, thing):
        self._write("list", id(thing), len(thing))
        for item in thing:
            self.save(item)

    def save_set(self, thing):
        self._write("set", id(thing), len(thing))
        for item in thing:
            self.save(item)

    def save_str(self, thing):
        lines = thing.split("\n")
        self._write("str", id(thing), len(lines))
        for line in lines:
            print(line, file=self.writer)

    def save_dict(self, thing):
        self._write("dict", id(thing), len(thing))
        for (key, value) in thing.items():
            self.save(key)
            self.save(value)


class LoadAlias(LoadOop):
    def __init__(self, reader):
        super().__init__(reader)
        self.seen = {}

    def load(self):
        line = self.reader.readline()[:-1]
        assert line, "Nothing to read"
        fields = line.split(":", maxsplit=2)
        assert len(fields) == 3, f"Badly-formed line {line}"
        key, ident, value = fields

        if key == "alias":
            assert ident in self.seen
            return self.seen[ident]

        method = f"load_{key}"
        assert hasattr(self, method), f"Unknown object type {key}"
        return getattr(self, method)(ident, value)

    def load_bool(self, ident, value):
        return super()._bool(value)

    def load_float(self, ident, value):
        return super()._float(value)

    def load_int(self, ident, value):
        return super()._int(value)

    def load_str(self, ident, value):
        return super()._str(value)

    # [load_list]
    def load_list(self, ident, value):
        result = []
        self.seen[ident] = result
        for _ in range(int(value)):
            result.append(self.load())
        return result
    # [/load_list]

    def load_set(self, ident, value):
        result = set()
        self.seen[ident] = result
        for _ in range(int(value)):
            result.add(self.load())
        return result

    def load_dict(self, ident, value):
        result = {}
        self.seen[ident] = result
        for _ in range(int(value)):
            k = self.load()
            v = self.load()
            result[k] = v
        return result
