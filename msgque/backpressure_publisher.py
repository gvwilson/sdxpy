from asimpy import Process
from message import Message
from backpressure_broker import BackpressureBroker


# mccole:init
class BackpressurePublisher(Process):
    """Publisher that adapts to backpressure signals."""

    def init(
        self,
        broker: BackpressureBroker,
        name: str,
        topic: str,
        base_interval: float,
        backoff_multiplier: float = 2.0,
    ):
        self.broker = broker
        self.name = name
        self.topic = topic
        self.base_interval = base_interval
        self.backoff_multiplier = backoff_multiplier
        self.message_counter = 0
        self.current_interval = base_interval
        self.backpressure_events = 0

    # mccole:/init

    # mccole:run
    async def run(self):
        """Generate and publish messages, slowing down on backpressure."""
        while True:
            # Create message.
            self.message_counter += 1
            message = Message(
                topic=self.topic,
                content=f"Message {self.message_counter} from {self.name}",
                id=self.message_counter,
                timestamp=self.now,
            )

            # Publish message and check if it was delivered.
            all_delivered = await self.broker.publish(message)

            if all_delivered:
                print(
                    f"[{self.now:.1f}] {self.name} published: {message.content} "
                    f"(interval: {self.current_interval:.1f}s)"
                )
                # Success - gradually return to base rate.
                if self.current_interval > self.base_interval:
                    self.current_interval = max(
                        self.base_interval, self.current_interval / 1.5
                    )
            else:
                # Backpressure detected - slow down.
                self.backpressure_events += 1
                self.current_interval *= self.backoff_multiplier
                print(
                    f"[{self.now:.1f}] {self.name} BACKPRESSURE - "
                    f"slowing to {self.current_interval:.1f}s interval"
                )

            # Wait before next message.
            await self.timeout(self.current_interval)

    # mccole:/run
