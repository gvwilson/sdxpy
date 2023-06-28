# [body]
class Env:
    def __init__(self, initial):
        self.stack = [initial.copy()]

    def push(self, frame):
        self.stack.append(frame)

    def pop(self):
        self.stack.pop()

    def find(self, name):
        for frame in reversed(self.stack):
            if name in frame:
                return frame[name]
        return None
# [/body]

    def __str__(self):
        return str(self.stack)
