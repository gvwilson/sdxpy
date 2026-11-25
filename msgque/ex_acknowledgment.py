"""Acknowledgment message queue simulation."""

import random
from asimpy import Environment, Process
from ack_broker import AckBroker
from message import Message
from dsdx import dsdx


# mccole:acksubscriber
class AckSubscriber(Process):
    """Subscriber that acknowledges messages (sometimes)."""

    def init(
        self,
        broker: AckBroker,
        name: str,
        topic: str,
        processing_time: float,
        failure_rate: float = 0.0,
    ):
        self.broker = broker
        self.name = name
        self.topic = topic
        self.processing_time = processing_time
        self.failure_rate = failure_rate
        self.num_received = 0
        self.num_acked = 0
        self.queue = broker.subscribe(topic)

    async def run(self):
        """Process messages and acknowledge them."""
        while True:
            message = await self.queue.get()
            self.num_received += 1

            print(
                f"[{self.now:.1f}] {self.name}: Received {message.content} "
                f"(ack_id {message.ack_id})"
            )

            # Simulate processing
            await self.timeout(self.processing_time)

            # Simulate occasional failures (don't acknowledge)
            if random.random() > self.failure_rate:
                self.broker.acknowledge(message.ack_id)
                self.num_acked += 1
                print(f"[{self.now:.1f}] {self.name}: Acknowledged {message.content}")
            else:
                print(
                    f"[{self.now:.1f}] {self.name}: FAILED to process "
                    f"{message.content} (will be redelivered)"
                )
# mccole:/acksubscriber


# mccole:ackpublisher
class AckPublisher(Process):
    """Simple publisher for acknowledgment test."""

    def init(self, broker: AckBroker, name: str, topic: str, interval: float):
        self.broker = broker
        self.name = name
        self.topic = topic
        self.interval = interval
        self.message_counter = 0

    async def run(self):
        """Publish messages at regular intervals."""
        while True:
            self.message_counter += 1
            message = Message(
                topic=self.topic,
                content=f"Message {self.message_counter} from {self.name}",
                id=self.message_counter,
                timestamp=self.now,
            )

            print(f"[{self.now:.1f}] {self.name}: Publishing {message.content}")
            await self.broker.publish(message)

            await self.timeout(self.interval)
# mccole:/ackpublisher


# mccole:simulate
def main():
    """Demonstrate acknowledgment-based redelivery."""
    env = Environment()

    # Create broker with 5-second timeout
    broker = AckBroker(env, ack_timeout=5.0)

    # Publisher
    AckPublisher(env, broker, "OrderService", "orders", interval=3.0)

    # Subscriber that sometimes fails to acknowledge (30% failure rate)
    subscriber = AckSubscriber(
        env, broker, "Processor", "orders", processing_time=1.0, failure_rate=0.3
    )

    # Run simulation
    env.run(until=25)

    print("\n=== Acknowledgment Statistics ===")
    print(f"Messages published: {broker.num_published}")
    print(f"Messages received: {subscriber.num_received}")
    print(f"Messages acknowledged: {subscriber.num_acked}")
    print(f"Pending acks: {len(broker.pending_acks)}")
# mccole:/simulate


if __name__ == "__main__":
    dsdx(main)
