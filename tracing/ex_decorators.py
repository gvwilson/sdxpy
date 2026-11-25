"""Example using decorator-based tracing."""

from asimpy import Environment, Process, Queue
from trace_collector import TraceCollector
from simple_service import SimpleService
from tracing_types import TraceContext, Span, ServiceRequest, generate_id
from tracing_decorators import Storage
from dsdx import dsdx


# mccole:client
class SimpleClient(Process):
    """Client that initiates traced requests."""

    def init(self, name: str, service: SimpleService, collector: TraceCollector):
        self.name = name
        self.service = service
        self.collector = collector
        Storage.set_collector(collector)

    async def run(self) -> None:
        """Generate requests."""
        for i in range(3):
            await self.timeout(1.5)
            await self.make_request(f"req_{i + 1}")

    async def make_request(self, req_id: str) -> None:
        """Make a traced request."""
        # Create trace
        trace_id = generate_id("trace_")
        root_span_id = generate_id("span_")

        print(f"\n[{self.now:.1f}] {self.name}: Starting request {req_id}")

        # Create root span
        root_span = Span(
            trace_id=trace_id,
            span_id=root_span_id,
            parent_span_id=None,
            operation_name=f"{self.name}.make_request",
            service_name=self.name,
            start_time=self.now,
        )

        # Create context
        context = TraceContext(
            trace_id=trace_id,
            span_id=root_span_id,
        )

        # Set context
        Storage.set_context(context)

        # Call service
        response_queue = Queue(self._env)
        request = ServiceRequest(
            request_id=req_id,
            context=context,
            payload={"data": f"request_{req_id}"},
            response_queue=response_queue,
        )

        await self.service.request_queue.put(request)
        response = await response_queue.get()

        # Finish root span
        root_span.finish(self.now)
        root_span.add_tag("success", response.success)
        await self.collector.span_queue.put(root_span)
# mccole:/client


# mccole:demo
def main() -> None:
    """Demonstrate decorator-based tracing."""
    env = Environment()

    # Create collector (quiet mode)
    collector = TraceCollector(env, verbose=False)

    # Create service with decorator-based instrumentation
    service = SimpleService(env, "OrderService", collector)

    # Create client
    SimpleClient(env, "Client", service, collector)

    # Run
    env.run(until=6)

    # Print results
    print("\n" + "=" * 60)
    print("Decorator-Based Tracing Results:")
    print("=" * 60)
    print(f"Traces completed: {collector.traces_completed}")
    print(f"Spans received: {collector.spans_received}")

    # Show traces
    for trace in collector.completed_traces:
        print(f"\n{trace}")
        duration = trace.get_duration()
        if duration:
            print(f"  Duration: {duration:.3f}s")
        print(f"  Spans: {len(trace.spans)}")

        # Show span names
        print("  Operations:")
        for span in sorted(trace.spans, key=lambda s: s.start_time):
            indent = "    " if span.parent_span_id else "  "
            print(f"{indent}- {span.operation_name} ({span.duration:.3f}s)")
# mccole:/demo


if __name__ == "__main__":
    dsdx(main)
