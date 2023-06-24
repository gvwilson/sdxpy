import string

from insert_delete import InsertDeleteApp


class Action:
    def __init__(self, app):
        self._app = app

    def do(self):
        raise NotImplementedError(f"{self.__class__.__name__}: do")

    def undo(self):
        raise NotImplementedError(f"{self.__class__.__name__}: undo")

    def save(self):
        return True


class Insert(Action):
    def __init__(self, app, pos, char):
        super().__init__(app)
        self._pos = pos
        self._char = char

    def do(self):
        self._app._buffer.insert(self._pos, self._char)

    def undo(self):
        self._app._buffer.delete(self._pos)

    def __str__(self):
        return f"Insert({self._pos}, '{self._char}')"


class Delete(Action):
    def __init__(self, app, pos):
        super().__init__(app)
        self._pos = pos
        self._char = self._app._buffer.char(pos)

    def do(self):
        self._app._buffer.delete(self._pos)

    def undo(self):
        self._app._buffer.insert(self._pos, self._char)

    def __str__(self):
        return f"Delete({self._pos}, '{self._char}')"


class Move(Action):
    def __init__(self, app, direction):
        super().__init__(app)
        self._direction = direction
        self._old = self._app._cursor.pos()
        self._new = None

    def do(self):
        self._app._cursor.act(self._direction)
        self._new = self._app._cursor.pos()

    def undo(self):
        self._app._cursor.move_to(self._old)

    def __str__(self):
        return f"Move('{self._direction}', {self._old}, {self._new})"


class Exit(Action):
    def do(self):
        self._app._running = False

    def __str__(self):
        return f"Exit()"


class ActionApp(InsertDeleteApp):
    INSERTABLE = set(string.ascii_letters + string.digits)

    def __init__(self, size, keystrokes):
        super().__init__(size, keystrokes)
        self._history = []

    def get_history(self):
        return self._history

    def _get_key(self):
        key = self._screen.getkey()
        if key in self.INSERTABLE:
            return "INSERT", key
        else:
            return None, key

    def _interact(self):
        family, key = self._get_key()
        name = f"_do_{family}" if family else f"_do_{key}"
        if not hasattr(self, name):
            return
        action = getattr(self, name)(key)
        self._history.append(action)
        action.do()
        self._add_log(key)

    def _add_log(self, key):
        self._log.append((key, self._cursor.pos(), self._screen.display()))

    def _do_DELETE(self, key):
        return Delete(self, self._cursor.pos())

    def _do_INSERT(self, key):
        return Insert(self, self._cursor.pos(), key)

    def _do_CONTROL_X(self, key):
        return Exit(self)

    def _do_KEY_UP(self, key):
        return Move(self, "up")

    def _do_KEY_DOWN(self, key):
        return Move(self, "down")

    def _do_KEY_LEFT(self, key):
        return Move(self, "left")

    def _do_KEY_RIGHT(self, key):
        return Move(self, "right")

    def _do_UNDO(self, key):
        return Undo(self)
