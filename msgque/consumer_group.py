from asimpy import Environment, Process, Queue
from broker import MessageBroker


# mccole:consumer
class ConsumerGroup:
    """Distribute messages among multiple consumers."""

    def __init__(
        self, env: Environment, broker: MessageBroker, topic: str, num_consumers: int
    ):
        self.env = env
        self.queue = broker.subscribe(topic)
        self.consumers = []

        # Create consumer queues for load balancing
        for i in range(num_consumers):
            consumer_queue = Queue(env)
            self.consumers.append(consumer_queue)

        # Start distributor process
        self._distributor = _Distributor(env, self.queue, self.consumers)

    def get_consumer_queue(self, index: int) -> Queue:
        """Get queue for a specific consumer in the group."""
        return self.consumers[index]


# mccole:/consumer


# mccole:distributor
class _Distributor(Process):
    """Distribute messages round-robin to consumers."""

    def init(self, source: Queue, destinations: list[Queue]):
        self.source = source
        self.destinations = destinations
        self.next_dest = 0

    async def run(self):
        """Forward messages to consumers in round-robin order."""
        while True:
            message = await self.source.get()
            dest = self.destinations[self.next_dest]
            await dest.put(message)
            self.next_dest = (self.next_dest + 1) % len(self.destinations)


# mccole:/distributor
