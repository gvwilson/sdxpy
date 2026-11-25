"""Distributed tracing with sampling and cross-service context propagation.

This module addresses two gaps in the basic tracing implementation:

1. Sampling:
   Recording every trace is expensive—storage, bandwidth, and CPU.
   Real systems sample: they record a fraction of traces and discard the rest.
   Head-based sampling decides at the start of a trace whether to record it.
   Tail-based sampling buffers the trace and decides at the end (after seeing
   the latency), allowing it to always record slow or errored requests.
   We implement head-based sampling here because it is simpler and sufficient
   for most use cases.

2. Cross-service propagation:
   In a real microservices system, services run in different processes.
   The only way to propagate trace context is to include it in the request—
   conventionally as HTTP headers:
       X-Trace-Id: abc123
       X-Span-Id: def456
       X-Parent-Span-Id: ghi789
   We simulate this by attaching the context to messages rather than relying
   on a shared global variable.

3. Thread safety:
   The basic tracer uses a module-level variable for the active context.
   This is fine for single-threaded, event-driven code (like our asimpy
   simulations), but in a real async or multi-threaded service each
   concurrent request needs its own context.  Python 3.7+ provides
   `contextvars.ContextVar` for this:

       _active_span: ContextVar[TraceContext | None] = ContextVar(
           "_active_span", default=None
       )

   Each asyncio task (and each OS thread) automatically gets its own copy
   of a ContextVar, so context from one request cannot leak into another.
   Our simulation is single-threaded, so we use a simple dict keyed by
   service name instead—but the principle is the same.
"""

import random
from dataclasses import dataclass
from asimpy import Process, Queue
from tracing_types import TraceContext, Span, generate_id, BaseCollector


# mccole:sampler
class HeadSampler:
    """Decides at trace start whether to record this trace.

    Head-based sampling uses a fixed probability per trace.
    Every span in a sampled trace is recorded; spans from unsampled traces
    are discarded immediately.

    Advantages: simple, low overhead, no buffering required.
    Disadvantages: slow/erroneous traces are as likely to be dropped as fast ones.
    For production use, tail-based sampling (buffer then decide) is more useful
    for diagnosing performance problems, but requires buffering all spans briefly.
    """

    def __init__(self, rate: float = 0.1) -> None:
        """rate: fraction of traces to record, 0.0 to 1.0."""
        if not 0.0 <= rate <= 1.0:
            raise ValueError(f"Sample rate must be between 0.0 and 1.0, got {rate}")
        self.rate = rate
        self.total_traces = 0
        self.sampled_traces = 0

    def should_sample(self) -> bool:
        """Return True if this trace should be recorded."""
        self.total_traces += 1
        if random.random() < self.rate:
            self.sampled_traces += 1
            return True
        return False

    def sample_rate_actual(self) -> float:
        """Observed sampling rate (may differ from target due to randomness)."""
        if self.total_traces == 0:
            return 0.0
        return self.sampled_traces / self.total_traces
# mccole:/sampler


# mccole:propagated_context
@dataclass
class PropagatedRequest:
    """A request that carries trace context for cross-service propagation.

    In a real HTTP system these fields would be HTTP headers:
        X-Trace-Id, X-Span-Id, X-Parent-Span-Id
    Attaching them to the message (rather than storing them globally)
    ensures that each concurrent request has its own context and
    context from one request cannot bleed into another.
    """

    request_id: str
    payload: dict
    response_queue: Queue
    # Trace context propagated from the caller, or None if not sampled.
    trace_context: TraceContext | None = None
# mccole:/propagated_context


# mccole:sampled_service
class SampledService(Process):
    """Service that applies head-based sampling before creating spans.

    When a request arrives with a trace context, the context dictates whether
    to record spans (the sampling decision was made by the initiating service).
    When a request arrives with no context (this service initiates the trace),
    the sampler decides.
    """

    def init(
        self,
        service_name: str,
        collector: BaseCollector,
        sampler: HeadSampler,
        downstream: "SampledService | None" = None,
    ) -> None:
        self.service_name = service_name
        self.collector = collector
        self.sampler = sampler
        self.downstream = downstream
        self.request_queue: Queue = Queue(self._env)

    async def run(self) -> None:
        while True:
            req: PropagatedRequest = await self.request_queue.get()
            await self._handle(req)

    async def _handle(self, req: PropagatedRequest) -> None:
        """Handle request, creating a span only if this trace is sampled."""
        ctx = req.trace_context

        # If no context, this service initiates the trace.
        if ctx is None:
            if self.sampler.should_sample():
                trace_id = generate_id("trace_")
                span_id = generate_id("span_")
                ctx = TraceContext(trace_id=trace_id, span_id=span_id)
            # else: not sampled — ctx stays None

        span: Span | None = None
        if ctx is not None:
            span = Span(
                trace_id=ctx.trace_id,
                span_id=generate_id("span_"),
                parent_span_id=ctx.span_id,
                operation_name=f"{self.service_name}.handle",
                service_name=self.service_name,
                start_time=self.now,
            )
            # Create a child context for downstream propagation.
            child_ctx = TraceContext(
                trace_id=ctx.trace_id,
                span_id=span.span_id,
                parent_span_id=ctx.span_id,
            )
        else:
            child_ctx = None

        # Simulate work.
        await self.timeout(random.uniform(0.1, 0.3))

        # Call downstream service if present, propagating the trace context.
        if self.downstream is not None:
            downstream_req = PropagatedRequest(
                request_id=req.request_id,
                payload=req.payload,
                response_queue=Queue(self._env),
                trace_context=child_ctx,  # propagated via message, not global state
            )
            await self.downstream.request_queue.put(downstream_req)
            await downstream_req.response_queue.get()

        # Finish and record span.
        if span is not None and ctx is not None:
            span.finish(self.now)
            await self.collector.span_queue.put(span)
            if child_ctx is not None:
                print(
                    f"[{self.now:.2f}] {self.service_name}: Recorded span "
                    f"trace={ctx.trace_id[:8]}... "
                    f"(sampled={self.sampler.rate:.0%})"
                )

        await req.response_queue.put({"ok": True})
# mccole:/sampled_service
