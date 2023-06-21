from insert_delete import InsertDeleteApp

class HistoryApp(InsertDeleteApp):
    def __init__(self, size, keystrokes):
        super().__init__(size, keystrokes)
        self._history = []

    def get_history(self):
        return self._history

    def _do_DELETE(self):
        row, col = self._cursor.pos()
        char = self._buffer.char((row, col))
        self._history.append(("delete", (row, col), char))
        self._buffer.delete(self._cursor.pos())

    def _do_INSERT(self, key):
        pos = self._cursor.pos()
        self._history.append(("insert", pos, key))
        self._buffer.insert(self._cursor.pos(), key)
