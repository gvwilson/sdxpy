"""Task generator for spawning simulations."""

import random
from asimpy import Process
from scheduler import WorkStealingScheduler


# mccole:gen
class TaskGenerator(Process):
    """Generates tasks including ones that spawn subtasks."""

    def init(self, scheduler: WorkStealingScheduler, num_initial_tasks: int):
        self.scheduler = scheduler
        self.num_initial_tasks = num_initial_tasks

    async def run(self):
        """Generate initial tasks."""
        for i in range(self.num_initial_tasks):
            self.scheduler.submit_task(duration=random.uniform(1.0, 3.0))
            await self.timeout(0.5)


# mccole:/gen
