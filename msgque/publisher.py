from asimpy import Process
from message import Message
from broker import MessageBroker


# mccole:publisher
class Publisher(Process):
    """Publishes messages to topics."""

    def init(self, broker: MessageBroker, name: str, topic: str, interval: float):
        self.broker = broker
        self.name = name
        self.topic = topic
        self.interval = interval
        self.message_counter = 0

    async def run(self):
        while True:
            self.message_counter += 1
            message = Message(
                topic=self.topic,
                content=f"Message {self.message_counter} from {self.name}",
                id=self.message_counter,
                timestamp=self.now,
            )

            print(f"[{self.now:.1f}] {self.name} publishing: {message.content}")
            await self.broker.publish(message)

            await self.timeout(self.interval)


# mccole:/publisher
