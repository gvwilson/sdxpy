from asimpy import FirstOf, Process
from broker import MessageBroker


# mccole:subscriber
class Subscriber(Process):
    """Subscribes to topics and processes messages."""

    def init(
        self,
        broker: MessageBroker,
        name: str,
        topics: list[str],
        processing_time: float,
    ):
        self.broker = broker
        self.name = name
        self.topics = topics
        self.processing_time = processing_time
        self.num_received = 0

        self.queues = {}
        for topic in topics:
            queue = broker.subscribe(topic)
            self.queues[topic] = queue

    async def run(self):
        while True:
            # Wait for a message from any queue.
            get_operations = {
                topic: queue.get() for topic, queue in self.queues.items()
            }
            topic, message = await FirstOf(self._env, **get_operations)

            # Report.
            self.num_received += 1
            latency = self.now - message.timestamp
            print(
                f"[{self.now:.1f}] {self.name} received from '{topic}': "
                f"{message.content} (latency: {latency:.1f})"
            )

            # Simulate processing time.
            await self.timeout(self.processing_time)


# mccole:/subscriber
