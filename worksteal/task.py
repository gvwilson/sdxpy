"""Task representation for work-stealing scheduler."""

from dataclasses import dataclass


# mccole:task
@dataclass
class Task:
    """A unit of work to be executed."""

    task_id: str
    duration: float
    parent_id: str | None = None  # For nested tasks

    def __str__(self):
        return f"Task({self.task_id})"


# mccole:/task
