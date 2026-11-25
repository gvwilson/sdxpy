"""MapReduce worker process."""

from asimpy import Process, Queue
import random
from typing import TYPE_CHECKING
from mr_types import MapTask, ReduceTask, IntermediateData

if TYPE_CHECKING:
    from mr_coordinator import MapReduceCoordinator


MAP_TIME = 0.1
REDUCE_TIME = 0.1


# mccole:worker
class MapReduceWorker(Process):
    """Worker that executes map and reduce tasks."""

    def init(self, worker_id: int, coordinator: "MapReduceCoordinator"):
        self.worker_id = worker_id
        self.coordinator = coordinator
        self.task_queue = Queue(self._env)
        self.current_task = None

        # Statistics
        self.maps_executed = 0
        self.reduces_executed = 0

        # Simulate failure probability
        self.failure_rate = 0.0

    # mccole:/worker

    # mccole:run
    async def run(self):
        """Main worker loop: fetch and execute tasks."""
        while True:
            # Get task from queue
            task = await self.task_queue.get()

            # Check for simulated failure
            if random.random() < self.failure_rate:
                print(f"[{self.now:.1f}] Worker {self.worker_id}: FAILED during {task}")
                await self.coordinator.report_failure(task, self.worker_id)
                continue

            # Execute task
            if isinstance(task, MapTask):
                await self.execute_map(task)
            elif isinstance(task, ReduceTask):
                await self.execute_reduce(task)

    # mccole:/run

    # mccole:map
    async def execute_map(self, task: MapTask):
        """Execute a map task."""
        self.current_task = task
        self.maps_executed += 1

        print(
            f"[{self.now:.1f}] Worker {self.worker_id}: "
            f"Starting {task} with {len(task.data)} records"
        )

        # Simulate processing time
        processing_time = len(task.data) * MAP_TIME
        await self.timeout(processing_time)

        # Apply map function
        intermediate = IntermediateData()
        for record in task.data:
            for key, value in self.coordinator.map_fn(record):
                intermediate.add(key, value)

        # Partition intermediate data
        partitions = intermediate.partition(self.coordinator.num_reducers)

        print(
            f"[{self.now:.1f}] Worker {self.worker_id}: "
            f"Completed {task}, produced {len(intermediate.pairs)} pairs"
        )

        # Send results to coordinator
        self.coordinator.map_completed(task.task_id, partitions, self.worker_id)

        self.current_task = None

    # mccole:/map

    # mccole:reduce
    async def execute_reduce(self, task: ReduceTask):
        """Execute a reduce task."""
        self.current_task = task
        self.reduces_executed += 1

        print(f"[{self.now:.1f}] Worker {self.worker_id}: Starting {task}")

        # Fetch intermediate data for this partition
        intermediate_data = await self.coordinator.get_intermediate_data(
            task.partition_id
        )

        # Group by key
        grouped = intermediate_data.group_by_key()

        print(
            f"[{self.now:.1f}] Worker {self.worker_id}: Processing {len(grouped)} keys"
        )

        # Simulate processing time
        processing_time = len(grouped) * REDUCE_TIME
        await self.timeout(processing_time)

        # Apply reduce function
        results = []
        for key, values in grouped.items():
            result = self.coordinator.reduce_fn(key, values)
            results.append((key, result))

        print(
            f"[{self.now:.1f}] Worker {self.worker_id}: "
            f"Completed {task}, produced {len(results)} results"
        )

        # Send results to coordinator
        self.coordinator.reduce_completed(task.task_id, results, self.worker_id)

        self.current_task = None


# mccole:/reduce
