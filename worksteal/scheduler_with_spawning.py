"""Scheduler using workers that can spawn tasks."""

from asimpy import Environment
from scheduler import WorkStealingScheduler
from worker_with_spawning import WorkerWithSpawning


# mccole:scheduler
class SchedulerWithSpawning(WorkStealingScheduler):
    """Scheduler using workers that can spawn tasks."""

    def __init__(
        self,
        env: Environment,
        num_workers: int,
        verbose: bool = True,
        worker_cls: type = WorkerWithSpawning,
    ):
        super().__init__(env, num_workers, verbose, worker_cls)


# mccole:/scheduler
