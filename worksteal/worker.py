"""Worker process for work-stealing scheduler."""

import random
from typing import TYPE_CHECKING
from asimpy import Process
from task import Task
from worker_deque import WorkerDeque

if TYPE_CHECKING:
    from scheduler import WorkStealingScheduler


# mccole:worker
class Worker(Process):
    """Worker that executes tasks with work-stealing."""

    def init(
        self, worker_id: int, scheduler: "WorkStealingScheduler", verbose: bool = True
    ):
        self.worker_id = worker_id
        self.scheduler = scheduler
        self.verbose = verbose
        self.deque = WorkerDeque()
        self.current_task: Task | None = None
        self.tasks_executed = 0
        self.tasks_stolen = 0

    # mccole:/worker

    # mccole:run
    async def run(self):
        """Main worker loop: execute local tasks or steal."""
        while True:
            # Try to get a task from local deque
            task = self.deque.pop_bottom()

            if task:
                # Execute local task
                await self.execute_task(task)
            else:
                # No local work, try stealing
                stolen = await self.try_steal()
                if stolen:
                    await self.execute_task(stolen)
                else:
                    # No work available anywhere, wait a bit
                    await self.timeout(0.1)

    # mccole:/run

    # mccole:execute
    async def execute_task(self, task: Task):
        """Execute a task."""
        self.current_task = task
        self.tasks_executed += 1
        if self.verbose:
            print(
                f"[{self.now:.1f}] Worker {self.worker_id}: "
                f"Executing {task.task_id} (queue size: {self.deque.size()})"
            )

        await self.timeout(task.duration)

        if self.verbose:
            print(f"[{self.now:.1f}] Worker {self.worker_id}: Completed {task.task_id}")
        self.current_task = None

    # mccole:/execute

    # mccole:steal
    async def try_steal(self) -> Task | None:
        """Try to steal a task from another worker."""
        targets = [w for w in self.scheduler.workers if w != self]
        if not targets:
            return None

        random.shuffle(targets)

        for target in targets:
            task = target.deque.steal_top()
            if task:
                self.tasks_stolen += 1
                if self.verbose:
                    print(
                        f"[{self.now:.1f}] Worker {self.worker_id}: "
                        f"Stole {task.task_id} from Worker {target.worker_id}"
                    )
                return task

        return None

    # mccole:/steal
