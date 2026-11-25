"""Request and response message types for the key-value store."""

from dataclasses import dataclass
from typing import Any
from asimpy import Queue
from vector_clock import VectorClock
from versioned_value import VersionedValue


# mccole:messages
@dataclass
class ReadRequest:
    """Request to read a key."""

    key: str
    client_id: str
    response_queue: Queue


@dataclass
class WriteRequest:
    """Request to write a key."""

    key: str
    value: Any
    context: VectorClock | None  # Client's version context
    client_id: str
    response_queue: Queue


@dataclass
class ReadResponse:
    """Response to a read request."""

    key: str
    versions: list[VersionedValue]  # May have multiple concurrent versions


@dataclass
class WriteResponse:
    """Response to a write request."""

    key: str
    success: bool
    clock: VectorClock
# mccole:/messages
