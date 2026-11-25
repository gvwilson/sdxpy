"""Worker that can spawn child tasks during execution."""

import random
from worker import Worker
from task import Task


# mccole:spawner
class WorkerWithSpawning(Worker):
    """Worker that can spawn child tasks during execution."""

    async def execute_task(self, task: Task):
        """Execute task and possibly spawn children."""
        self.current_task = task
        self.tasks_executed += 1

        print(f"[{self.now:.1f}] Worker {self.worker_id}: Executing {task.task_id}")

        # Do half the work
        await self.timeout(task.duration / 2)

        # Randomly spawn child tasks (simulating divide-and-conquer)
        if random.random() < 0.3:  # 30% chance
            num_children = random.randint(1, 3)
            for i in range(num_children):
                child = Task(
                    task_id=f"{task.task_id}.{i}",
                    duration=random.uniform(0.3, 1.0),
                    parent_id=task.task_id,
                )
                self.spawn_task(child)

        # Finish the work
        await self.timeout(task.duration / 2)

        print(f"[{self.now:.1f}] Worker {self.worker_id}: Completed {task.task_id}")

        self.current_task = None

    def spawn_task(self, task: Task):
        """Spawn a new task (called by executing task)."""
        self.deque.push_bottom(task)
        print(f"[{self.now:.1f}] Worker {self.worker_id}: Spawned {task.task_id}")


# mccole:/spawner
