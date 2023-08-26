# [save]
class SaveObjects:
    def __init__(self, writer):
        self.writer = writer

    def save(self, thing):
        typename = type(thing).__name__
        method = f"save_{typename}"
        assert hasattr(self, method), \
            f"Unknown object type {typename}"
        getattr(self, method)(thing)
# [/save]

    def _write(self, *fields):
        print(":".join(str(f) for f in fields), file=self.writer)

    def save_bool(self, thing):
        self._write("bool", thing)

    def save_float(self, thing):
        self._write("float", thing)

    # [save_examples]
    def save_int(self, thing):
        self._write("int", thing)

    def save_str(self, thing):
        lines = thing.split("\n")
        self._write("str", len(lines))
        for line in lines:
            print(line, file=self.writer)
    # [/save_examples]

    def save_list(self, thing):
        self._write("list", len(thing))
        for item in thing:
            self.save(item)

    def save_set(self, thing):
        self._write("set", len(thing))
        for item in thing:
            self.save(item)

    def save_dict(self, thing):
        self._write("dict", len(thing))
        for (key, value) in thing.items():
            self.save(key)
            self.save(value)


# [load]
class LoadObjects:
    def __init__(self, reader):
        self.reader = reader

    def load(self):
        line = self.reader.readline()[:-1]
        assert line, "Nothing to read"
        fields = line.split(":", maxsplit=1)
        assert len(fields) == 2, f"Badly-formed line {line}"
        key, value = fields
        method = f"load_{key}"
        assert hasattr(self, method), f"Unknown object type {key}"
        return getattr(self, method)(value)
    # [/load]

    def load_bool(self, value):
        names = {"True": True, "False": False}
        assert value in names, f"Unknown Boolean {value}"
        return names[value]

    # [load_float]
    def load_float(self, value):
        return float(value)
    # [/load_float]

    def load_int(self, value):
        return int(value)

    def load_str(self, value):
        return "\n".join(
            [self.reader.readline()[:-1] for _ in range(int(value))]
        )

    # [load_list]
    def load_list(self, value):
        return [self.load() for _ in range(int(value))]
    # [/load_list]

    def load_set(self, value):
        return {self.load() for _ in range(int(value))}

    def load_dict(self, value):
        result = {}
        for _ in range(int(value)):
            k = self.load()
            v = self.load()
            result[k] = v
        return result
