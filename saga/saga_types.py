"""Data types for Saga pattern implementation."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from enum import Enum


# mccole:enum
class SagaStatus(Enum):
    """Status of a saga execution."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


class TransactionStatus(Enum):
    """Status of individual transaction."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"
# mccole:/enum


# mccole:sagatypes
@dataclass
class SagaStep:
    """A step in the saga with transaction and compensation."""

    name: str
    service_name: str
    transaction: Callable[[], bool]  # Returns True if successful
    compensation: Optional[Callable[[], bool]]  # Returns True if successful

    def __str__(self) -> str:
        return f"Step({self.name})"


@dataclass
class SagaExecution:
    """Tracks execution of a saga instance."""

    saga_id: str
    steps: List[SagaStep]
    status: SagaStatus = SagaStatus.PENDING
    current_step: int = 0
    completed_steps: List[str] = field(default_factory=list)
    failed_step: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"Saga({self.saga_id}, {self.status.value}, step {self.current_step}/{len(self.steps)})"


@dataclass
class BookingRequest:
    """Travel booking request."""

    booking_id: str
    customer_id: str
    flight_id: str
    hotel_id: str
    car_id: str

    def __str__(self) -> str:
        return f"Booking({self.booking_id})"


@dataclass
class SagaEvent:
    """Event in choreographed saga."""

    event_type: str  # "flight_booked", "flight_failed", etc.
    saga_id: str
    data: Dict[str, Any]

    def __str__(self) -> str:
        return f"Event({self.event_type})"
# mccole:/sagatypes
