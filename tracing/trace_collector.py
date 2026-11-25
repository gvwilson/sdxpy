"""Trace collector for aggregating spans into traces."""

from asimpy import Queue
from tracing_types import BaseCollector, Span, Trace


# mccole:collector
class TraceCollector(BaseCollector):
    """Collects and aggregates spans into traces."""

    def init(self, verbose=True) -> None:
        self.verbose = verbose
        self.span_queue: Queue = Queue(self._env)
        self.active_traces: dict[str, Trace] = {}
        self.completed_traces: list[Trace] = []

        # Statistics
        self.spans_received = 0
        self.traces_completed = 0

    async def run(self) -> None:
        """Main collector loop."""
        print(f"[{self.now:.1f}] TraceCollector started")
        while True:
            span = await self.span_queue.get()
            self.process_span(span)

    # mccole:/collector

    # mccole:process
    def process_span(self, span: Span) -> None:
        """Process incoming span."""
        self.spans_received += 1

        # Get or create trace
        if span.trace_id not in self.active_traces:
            self.active_traces[span.trace_id] = Trace(trace_id=span.trace_id)

        trace = self.active_traces[span.trace_id]
        trace.add_span(span)

        # Check if trace is complete
        if self.is_trace_complete(trace):
            self.complete_trace(trace)
            if self.verbose:
                self.report_trace(trace)
                self.print_span_tree(trace)

    def is_trace_complete(self, trace: Trace) -> bool:
        """Check if all spans in trace are finished."""
        if not trace.spans:
            return False
        return all(span.end_time is not None for span in trace.spans)

    def complete_trace(self, trace: Trace) -> None:
        """Mark trace as complete and move to storage."""
        self.completed_traces.append(trace)
        self.traces_completed += 1
        del self.active_traces[trace.trace_id]

    # mccole:/process

    def report_trace(self, trace: Trace) -> None:
        """Show newly-completed trace."""

        duration = trace.get_duration()
        print(f"\n[{self.now:.1f}] Completed {trace}")
        print(
            f"  Total duration: {duration:.3f}s" if duration else "  Duration: unknown"
        )
        print(f"  Spans: {len(trace.spans)}")

    def print_span_tree(self, trace: Trace) -> None:
        """Print span tree structure."""
        root = trace.get_root_span()
        if root:
            print("  Span tree:")
            self._print_span_recursive(trace, root, indent=2)

    def _print_span_recursive(self, trace: Trace, span: Span, indent: int) -> None:
        """Recursively print span and children."""
        prefix = " " * indent + "└─"
        duration_str = f"{span.duration:.3f}s" if span.duration else "?"
        print(f"{prefix} {span.operation_name} ({span.service_name}) - {duration_str}")

        children = [s for s in trace.spans if s.parent_span_id == span.span_id]
        for child in sorted(children, key=lambda s: s.start_time):
            self._print_span_recursive(trace, child, indent + 2)

    def get_slow_traces(self, threshold: float) -> list[Trace]:
        """Find traces slower than threshold."""
        slow = []
        for trace in self.completed_traces:
            duration = trace.get_duration()
            if duration and duration > threshold:
                slow.append(trace)
        return slow
