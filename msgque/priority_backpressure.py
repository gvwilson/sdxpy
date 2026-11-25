import bisect
from dataclasses import dataclass
from asimpy import Environment, Queue, PriorityQueue
from collections import defaultdict

from message import Message


# mccole:message
@dataclass
class PriorityMessage(Message):
    """Message with priority level."""

    priority: int = 0  # Lower number = higher priority

    def __lt__(self, other):
        """Compare by priority for heap operations."""
        return self.priority < other.priority


# mccole:/message


class PriorityBackpressureBroker:
    """Broker that uses priority queues with bounded capacity."""

    def __init__(self, env: Environment, max_queue_size: int = 10):
        self.env = env
        self.max_queue_size = max_queue_size
        self.topics: dict[str, list[Queue]] = defaultdict(list)
        self.num_published = 0
        self.num_delivered = 0

    def subscribe(self, topic: str) -> Queue:
        """Create a bounded priority queue for a subscriber to a topic."""
        queue = PriorityQueue(self.env, capacity=self.max_queue_size)
        self.topics[topic].append(queue)
        return queue

    # mccole:publish
    async def publish(self, message: PriorityMessage) -> bool:
        """Publish message to priority queues.

        Returns:
            True if message was accepted by all queues.
        """
        self.num_published += 1
        queues = self.topics.get(message.topic, [])

        all_delivered = True
        for queue in queues:
            if not queue.is_full():
                await queue.put(message)
                self.num_delivered += 1
            else:
                # Displace lowest priority item if new message has higher priority
                bisect.insort(queue._items, message)
                kept = message is not queue._items[-1]
                queue._items = queue._items[: queue._capacity]
                if kept:
                    self.num_delivered += 1
                else:
                    all_delivered = False

        return all_delivered

    # mccole:/publish
