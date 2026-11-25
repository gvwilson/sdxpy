"""Worker with adaptive target selection strategy."""

from typing import TYPE_CHECKING
from worker import Worker
from task import Task

if TYPE_CHECKING:
    from scheduler import WorkStealingScheduler


# mccole:worker
class AdaptiveWorker(Worker):
    """Worker with adaptive target selection."""

    def init(
        self, worker_id: int, scheduler: "WorkStealingScheduler", verbose: bool = True
    ):
        super().init(worker_id, scheduler)
        self.steal_attempts = 0
        self.failed_steals = 0

    async def try_steal(self) -> Task | None:
        """Try to steal with adaptive target selection."""
        self.steal_attempts += 1

        # Try workers with largest queues first
        targets = [w for w in self.scheduler.workers if w != self]
        targets.sort(key=lambda w: w.deque.size(), reverse=True)

        for target in targets:
            if target.deque.size() > 0:
                task = target.deque.steal_top()
                if task:
                    self.tasks_stolen += 1
                    print(
                        f"[{self.now:.1f}] Worker {self.worker_id}: "
                        f"Stole {task.task_id} from Worker {target.worker_id} "
                        f"(target queue: {target.deque.size()})"
                    )
                    return task

        self.failed_steals += 1
        return None


# mccole:/worker
