import string

from action import Action, ActionApp


# [Undo]
class Undo(Action):
    def do(self):
        action = self._app._history.pop()
        action.undo()

    def save(self):
        return False

    def __str__(self):
        return f"Undo({self._app._history[-1]})"
# [/Undo]


# [app]
class UndoableApp(ActionApp):
    # [skip]
    def _do_UNDO(self, key):
        return Undo(self)
    # [/skip]
    def _interact(self):
        family, key = self._get_key()
        name = f"_do_{family}" if family else f"_do_{key}"
        if not hasattr(self, name):
            return
        action = getattr(self, name)(key)
        action.do()
        if action.save():
            self._history.append(action)
        self._add_log(key)
# [/app]
