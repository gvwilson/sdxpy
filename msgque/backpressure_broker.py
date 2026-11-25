from asimpy import Environment, Queue
from collections import defaultdict

from message import Message


# mccole:backpressure
class BackpressureBroker:
    """A message broker with backpressure support."""

    def __init__(self, env: Environment, max_queue_size: int = 10):
        self.env = env
        self.max_queue_size = max_queue_size
        self.topics: dict[str, list[Queue]] = defaultdict(list)
        self.num_published = 0
        self.num_delivered = 0
        self.num_dropped = 0

    # mccole:/backpressure

    # mccole:subscribe
    def subscribe(self, topic: str) -> Queue:
        """Create a bounded queue for a subscriber to a topic."""
        queue = Queue(self.env, capacity=self.max_queue_size)
        self.topics[topic].append(queue)
        return queue

    # mccole:/subscribe

    # mccole:publish
    async def publish(self, message: Message) -> bool:
        """
        Publish a message, applying backpressure if queues are full.
        Returns True if message was delivered to all subscribers,
        False if any queue was full and message was dropped.
        """
        self.num_published += 1
        queues = self.topics.get(message.topic, [])

        all_delivered = True
        for queue in queues:
            if not queue.is_full():
                await queue.put(message)
                self.num_delivered += 1
            else:
                self.num_dropped += 1
                all_delivered = False

        return all_delivered

    # mccole:/publish
