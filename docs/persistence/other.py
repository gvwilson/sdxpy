from extend import LoadExtend, SaveExtend


class PersistenceError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class SaveOther(SaveExtend):
    def __init__(self, writer, handlers):
        super().__init__(writer)
        self.handlers = handlers
        self.methods = (self._aliased, self._builtin, self._extension, self._other)

    def save(self, thing):
        for method in self.methods:
            if method(thing):
                return
        raise PersistenceError(f"Don't know how to handle {thing}")

    def _other(self, thing):
        cls = thing.__class__
        if cls not in self.handlers:
            return False
        self._write("@other", id(thing), cls.__name__)
        handler = self.handlers[cls]
        as_dict = handler(thing)
        assert isinstance(as_dict, dict), f"Handler for {cls_name} didn't return dict"
        self.save(handler(thing))
        return True


class LoadOther(LoadExtend):
    def __init__(self, reader, extensions, handlers):
        super().__init__(reader, *extensions)
        self.handlers = {cls.__name__: func for cls, func in handlers.items()}
        self.methods = (self._aliased, self._builtin, self._extension, self._other)

    def load(self):
        key, ident, value = self._next()
        for method in self.methods:
            try:
                return method(key, ident, value)
            except KeyError:
                pass
        assert False, f"Don't know how to handle {key} {ident} {value}"

    def _other(self, key, ident, value):
        if (key != "@other") or (value not in self.handlers):
            raise KeyError()
        handler = self.handlers[value]
        contents = self.load()
        return handler(contents)
