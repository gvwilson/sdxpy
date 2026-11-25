"""Worker that waits for child tasks to complete before finishing the parent."""

import random
from typing import Dict
from asimpy import Queue
from task import Task
from worker import Worker


# mccole:joining
class JoiningWorker(Worker):
    """Worker that tracks parent-child relationships and waits for children.

    When a task spawns children, it does not complete until all children have
    finished.  This models the fork-join pattern used in parallel divide-and-conquer
    algorithms such as merge sort or parallel tree traversal.

    Hidden complexity note:
    In a real work-stealing runtime (e.g. Go's goroutine scheduler or Java's
    ForkJoin framework) this wait is implemented with a *continuation*: the
    parent task is suspended at the join point and placed back onto the deque
    so other workers can continue making progress.  The parent only resumes
    once a counter of outstanding children reaches zero.

    Our simulation uses asimpy queues to implement the same idea: the parent
    awaits a completion queue, and each child posts to that queue when it
    finishes.  Because asimpy is single-threaded (event-driven), there are no
    race conditions, but in a real concurrent system the counter decrement must
    be atomic to avoid the parent waking up before all children are done.
    """

    def init(self, worker_id: int, scheduler, verbose: bool = True):
        super().init(worker_id, scheduler, verbose)
        # Maps parent_id -> Queue that the parent is waiting on.
        # Each child posts to this queue when it completes.
        self.join_queues: Dict[str, Queue] = {}
        # Maps parent_id -> number of children still outstanding.
        self.pending_children: Dict[str, int] = {}

    async def execute_task(self, task: Task):
        """Execute task, spawn children, and wait for all of them to finish."""
        self.current_task = task
        self.tasks_executed += 1

        if self.verbose:
            print(
                f"[{self.now:.1f}] Worker {self.worker_id}: "
                f"Executing {task.task_id}"
            )

        # Do the first half of the work.
        await self.timeout(task.duration / 2)

        # Randomly spawn children (simulating divide-and-conquer).
        children_spawned: int = 0
        if random.random() < 0.4:
            num_children = random.randint(1, 3)
            # Create a queue that children will signal when they are done.
            join_queue: Queue = Queue(self._env)
            self.join_queues[task.task_id] = join_queue
            self.pending_children[task.task_id] = num_children

            for i in range(num_children):
                child = Task(
                    task_id=f"{task.task_id}.{i}",
                    duration=random.uniform(0.3, 0.8),
                    parent_id=task.task_id,
                )
                self.deque.push_bottom(child)
                children_spawned += 1
                if self.verbose:
                    print(
                        f"[{self.now:.1f}] Worker {self.worker_id}: "
                        f"Spawned child {child.task_id}"
                    )

        # If children were spawned, wait until all of them complete.
        if children_spawned > 0:
            join_queue = self.join_queues[task.task_id]
            while self.pending_children[task.task_id] > 0:
                await join_queue.get()
                # (Each child posts one item when it finishes.)

            del self.join_queues[task.task_id]
            del self.pending_children[task.task_id]

            if self.verbose:
                print(
                    f"[{self.now:.1f}] Worker {self.worker_id}: "
                    f"All children of {task.task_id} done; resuming parent"
                )

        # Do the second half of the work.
        await self.timeout(task.duration / 2)

        if self.verbose:
            print(
                f"[{self.now:.1f}] Worker {self.worker_id}: "
                f"Completed {task.task_id}"
            )

        self.current_task = None

        # Notify parent (if any) that this child is done.
        if task.parent_id is not None:
            # Find the worker that is waiting for this child.
            for worker in self.scheduler.workers:
                if (
                    isinstance(worker, JoiningWorker)
                    and task.parent_id in worker.join_queues
                ):
                    worker.pending_children[task.parent_id] -= 1
                    await worker.join_queues[task.parent_id].put(task.task_id)
                    break
# mccole:/joining
