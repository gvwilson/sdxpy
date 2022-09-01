from aliasing import SaveAlias, LoadAlias

# [save]
class SaveExtend(SaveAlias):
    def __init__(self, writer):
        super().__init__(writer)

    def save(self, thing):
        if self._aliased(thing):
            return
        if self._builtin(thing):
            return
        # [omit_extension]
        if self._extension(thing):
            return
        # [/omit_extension]
        assert False, f"Don't know how to handle {thing}"

    # [save_aliased]
    def _aliased(self, thing):
        thing_id = id(thing)
        if thing_id not in self.seen:
            return False
        self._write("alias", thing_id, "")
        return True
    # [/save_aliased]

    # [save_builtin]
    def _builtin(self, thing):
        typename = type(thing).__name__
        method = f"_{typename}"
        if not hasattr(self, method):
            return False
        self.seen.add(id(thing))
        getattr(self, method)(thing)
        return True
    # [/save_builtin]
# [/save]

    # [save_extension]
    def _extension(self, thing):
        if not hasattr(thing, "to_dict"):
            return False
        self._write("@extension", id(thing), thing.__class__.__name__)
        self.save(thing.to_dict())
        return True
    # [/save_extension]

# [load_constructor]
class LoadExtend(LoadAlias):
    def __init__(self, reader, *extensions):
        super().__init__(reader)
        self.seen = {}
        self.extensions = {e.__name__:e for e in extensions}
# [/load_constructor]

    # [load_load]
    def load(self):
        key, ident, value = self._next()
        for method in (self._aliased, self._builtin, self._extension):
            try:
                return method(key, ident, value)
            except KeyError:
                pass
        assert False, f"Don't know how to handle {key} {ident} {value}"
    # [/load_load]

    # [inherited]
    def _aliased(self, key, ident, value):
        if key != "alias":
            raise KeyError()
        assert ident in self.seen
        return self.seen[ident]

    def _builtin(self, key, ident, value):
        method = f"_{key}"
        if not hasattr(self, method):
            raise KeyError()
        return getattr(self, method)(ident, value)
    # [/inherited]

    # [load_extension]
    def _extension(self, key, ident, value):
        if (key != "@extension") or (value not in self.extensions):
            raise KeyError()
        cls = self.extensions[value]
        contents = self.load()
        return cls(**contents)
    # [/load_extension]
    
    def _next(self):
        line = self.reader.readline()[:-1]
        assert line, "Nothing to read"
        fields = line.split(":", maxsplit=2)
        assert len(fields) == 3, f"Badly-formed line {line}"
        return fields
