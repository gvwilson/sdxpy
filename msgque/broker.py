from asimpy import Environment, Queue
from collections import defaultdict

from message import Message


# mccole:broker
class MessageBroker:
    """A message broker that routes messages to topic subscribers."""

    def __init__(self, env: Environment):
        self.env = env
        self.topics: dict[str, list[Queue]] = defaultdict(list)
        self.num_published = 0
        self.num_delivered = 0

    # mccole:/broker

    # mccole:subscribe
    def subscribe(self, topic: str) -> Queue:
        """Create a queue for a subscriber to a topic."""
        queue = Queue(self.env)
        self.topics[topic].append(queue)
        return queue

    # mccole:/subscribe

    # mccole:publish
    async def publish(self, message: Message):
        """Publish a message to all subscribers of its topic."""
        self.num_published += 1
        queues = self.topics.get(message.topic, [])
        for queue in queues:
            await queue.put(message)
            self.num_delivered += 1

    # mccole:/publish
