from dataclasses import dataclass


# mccole:message
@dataclass
class Message:
    topic: str
    content: str
    id: int
    timestamp: float


# mccole:/message
