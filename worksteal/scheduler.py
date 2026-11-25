"""Work-stealing scheduler coordinator."""

import random
from asimpy import Environment
from task import Task
from worker import Worker


# mccole:scheduler
class WorkStealingScheduler:
    """Scheduler that coordinates work-stealing workers."""

    def __init__(
        self,
        env: Environment,
        num_workers: int,
        verbose: bool = True,
        worker_cls: type = Worker,
    ):
        self.env = env
        self.num_workers = num_workers
        self.verbose = verbose
        self.workers: list = []
        self.task_counter = 0

        # Create workers
        for i in range(num_workers):
            worker = worker_cls(env, i, self, verbose)
            self.workers.append(worker)

    def submit_task(self, duration: float, parent_id: str | None = None) -> Task:
        """Submit a task to a random worker."""
        self.task_counter += 1
        task = Task(
            task_id=f"T{self.task_counter}",
            duration=duration,
            parent_id=parent_id,
        )

        worker = random.choice(self.workers)
        worker.deque.push_bottom(task)

        if self.verbose:
            print(
                f"[{self.env.now:.1f}] Submitted {task.task_id} "
                f"to Worker {worker.worker_id}"
            )

        return task

    # mccole:/scheduler

    def get_statistics(self):
        """Get scheduler statistics."""
        total_executed = sum(w.tasks_executed for w in self.workers)
        total_stolen = sum(w.tasks_stolen for w in self.workers)

        print("\n=== Statistics ===")
        print(f"Total tasks executed: {total_executed}")
        print(f"Total tasks stolen: {total_stolen}")
        print(f"Steal rate: {100 * total_stolen / max(total_executed, 1):.1f}%")

        for worker in self.workers:
            print(
                f"Worker {worker.worker_id}: "
                f"executed={worker.tasks_executed}, "
                f"stolen={worker.tasks_stolen}, "
                f"queue={worker.deque.size()}"
            )
