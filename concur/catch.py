import greenlet


class FirstException(Exception):
    pass


class SecondException(Exception):
    pass


class Task(greenlet.greenlet):
    def __init__(self, excClass):
        self._excClass = excClass

    def run(self):
        raise self._excClass()


class Scheduler(greenlet.greenlet):
    def __init__(self, *tasks):
        self._queue = list(tasks)

    def run(self):
        while self._queue:
            task = self._queue.pop(0)
            try:
                task.switch()
                if not task.dead:
                    self._queue.append(task)
            except FirstException as exc:
                print('caught FirstException')


if __name__ == "__main__":
    scheduler = Scheduler(Task(FirstException), Task(SecondException))
    try:
        scheduler.run()
    except Exception as exc:
        print(f'scheduler did not catch {type(exc).__name__}')
