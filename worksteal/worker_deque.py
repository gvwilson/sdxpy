"""Double-ended queue for work-stealing."""

from task import Task


# mccole:deque
class WorkerDeque:
    """Double-ended queue for tasks with stealing support."""

    def __init__(self):
        self.tasks: list[Task] = []

    def push_bottom(self, task: Task):
        """Owner pushes task to bottom (private end)."""
        self.tasks.append(task)

    def pop_bottom(self) -> Task | None:
        """Owner pops task from bottom."""
        return self.tasks.pop() if self.tasks else None

    def steal_top(self) -> Task | None:
        """Thief steals task from top (public end)."""
        return self.tasks.pop(0) if self.tasks else None

    def is_empty(self) -> bool:
        """Check if deque is empty."""
        return len(self.tasks) == 0

    def size(self) -> int:
        """Return number of tasks."""
        return len(self.tasks)


# mccole:/deque
