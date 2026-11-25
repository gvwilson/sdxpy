"""Prioritized message queue simulation."""

import random
from asimpy import Environment, Process
from priority_backpressure import PriorityBackpressureBroker, PriorityMessage
from dsdx import dsdx


# mccole:prioritypublisher
class PriorityPublisher(Process):
    """Publisher that sends messages with different priorities."""

    def init(
        self,
        broker: PriorityBackpressureBroker,
        name: str,
        topic: str,
        interval: float,
    ):
        self.broker = broker
        self.name = name
        self.topic = topic
        self.interval = interval
        self.message_counter = 0

    async def run(self):
        """Publish messages with varying priorities."""
        while True:
            self.message_counter += 1

            # Assign priorities: 70% low (5-9), 30% high (0-4)
            if random.random() < 0.3:
                priority = random.randint(0, 4)  # High priority
            else:
                priority = random.randint(5, 9)  # Low priority

            message = PriorityMessage(
                topic=self.topic,
                content=f"Msg{self.message_counter}",
                id=self.message_counter,
                timestamp=self.now,
                priority=priority,
            )

            await self.broker.publish(message)
            print(
                f"[{self.now:.1f}] {self.name}: Published priority {priority} "
                f"{message.content}"
            )

            await self.timeout(self.interval)
# mccole:/prioritypublisher


# mccole:prioritysubscriber
class PrioritySubscriber(Process):
    """Subscriber that processes priority messages."""

    def init(
        self,
        broker: PriorityBackpressureBroker,
        name: str,
        topic: str,
        processing_time: float,
    ):
        self.broker = broker
        self.name = name
        self.topic = topic
        self.processing_time = processing_time
        self.num_received = 0
        self.priority_counts = {}
        self.queue = broker.subscribe(topic)

    async def run(self):
        """Process messages in priority order."""
        while True:
            message = await self.queue.get()

            self.num_received += 1
            priority = message.priority
            self.priority_counts[priority] = self.priority_counts.get(priority, 0) + 1

            print(
                f"[{self.now:.1f}] {self.name}: Processing priority {priority} "
                f"{message.content}"
            )

            await self.timeout(self.processing_time)
# mccole:/prioritysubscriber


# mccole:simulate
def main():
    """Demonstrate priority-based message handling."""
    env = Environment()

    # Small queue to trigger capacity limits quickly
    broker = PriorityBackpressureBroker(env, max_queue_size=5)

    # Fast publisher, slow subscriber creates backpressure
    PriorityPublisher(env, broker, "EventGen", "events", interval=0.3)
    subscriber = PrioritySubscriber(
        env, broker, "Processor", "events", processing_time=1.5
    )

    # Run simulation
    env.run(until=20)

    print("\n=== Priority Queue Statistics ===")
    print(f"Messages published: {broker.num_published}")
    print(f"Messages delivered: {broker.num_delivered}")
    print(f"Messages received: {subscriber.num_received}")

    print("\nReceived by priority:")
    for priority in sorted(subscriber.priority_counts.keys()):
        print(f"  Priority {priority}: {subscriber.priority_counts[priority]}")
# mccole:/simulate


if __name__ == "__main__":
    dsdx(main)
