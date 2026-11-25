"""Data types for distributed tracing implementation."""

from asimpy import Environment
from dataclasses import dataclass, field
import random
from typing import Any
from asimpy import Process, Queue


class BaseCollector(Process):
    pass


# mccole:context
@dataclass
class TraceContext:
    """Context propagated between services."""

    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    baggage: dict[str, str] = field(default_factory=dict)
    # mccole:/context

    def __str__(self) -> str:
        return f"TraceContext(trace={self.trace_id[:8]}..., span={self.span_id[:8]}...)"


# mccole:span
@dataclass
class Span:
    """Represents a unit of work in a trace."""

    trace_id: str
    span_id: str
    parent_span_id: str | None
    operation_name: str
    service_name: str
    start_time: float
    end_time: float | None = None
    duration: float | None = None
    tags: dict[str, Any] = field(default_factory=dict)
    logs: list[dict[str, Any]] = field(default_factory=list)

    def add_tag(self, key: str, value: Any) -> None:
        """Add metadata tag to span."""
        self.tags[key] = value

    def add_log(self, message: str, **fields: Any) -> None:
        """Add log entry to span."""
        self.logs.append(
            {"message": message, "timestamp": Environment.sim_time(), **fields}
        )

    def finish(self, end_time: float) -> None:
        """Mark span as complete."""
        self.end_time = end_time
        self.duration = end_time - self.start_time

    # mccole:/span

    def __str__(self) -> str:
        status = f"{self.duration:.3f}s" if self.duration else "active"
        return f"Span({self.operation_name}, {status})"


# mccole:trace
@dataclass
class Trace:
    """Complete trace containing all spans."""

    trace_id: str
    spans: list[Span] = field(default_factory=list)
    start_time: float | None = None
    end_time: float | None = None

    def add_span(self, span: Span) -> None:
        """Add span to trace."""
        self.spans.append(span)

        if self.start_time is None or span.start_time < self.start_time:
            self.start_time = span.start_time

        if span.end_time:
            if self.end_time is None or span.end_time > self.end_time:
                self.end_time = span.end_time

    def get_root_span(self) -> Span | None:
        """Get root span (no parent)."""
        for span in self.spans:
            if span.parent_span_id is None:
                return span
        return None

    def get_duration(self) -> float | None:
        """Get total trace duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    # mccole:/trace

    def __str__(self) -> str:
        duration = self.get_duration()
        status = f"{duration:.3f}s" if duration else "incomplete"
        return f"Trace({self.trace_id[:8]}..., {len(self.spans)} spans, {status})"


@dataclass
class ServiceRequest:
    """Request between services with trace context."""

    request_id: str
    context: TraceContext | None
    payload: dict[str, Any]
    response_queue: Queue

    def __str__(self) -> str:
        return f"Request({self.request_id})"


@dataclass
class ServiceResponse:
    """Response from service."""

    request_id: str
    success: bool
    data: Any = None
    error: str | None = None

    def __str__(self) -> str:
        status = "success" if self.success else f"error: {self.error}"
        return f"Response({self.request_id}, {status})"


def generate_id(prefix: str = "") -> str:
    """Generate unique ID for trace or span."""
    return f"{prefix}{random.randint(1000000, 9999999)}"
