"""Decorators for automatic distributed tracing instrumentation."""

from functools import wraps
from typing import Any, Callable
from tracing_types import BaseCollector, Span, TraceContext, generate_id


# mccole:storage
class _StorageClass:
    """Record trace information."""

    def __init__(self):
        """Construct instance."""
        self._current_context = None
        self._current_collector = None

    @classmethod
    def set_context(cls, context: TraceContext | None) -> None:
        Storage._current_context = context

    @classmethod
    def get_context(cls) -> TraceContext | None:
        return Storage._current_context

    @classmethod
    def set_collector(cls, collector: BaseCollector) -> None:
        Storage._current_collector = collector

    @classmethod
    def get_collector(cls) -> BaseCollector | None:
        return Storage._current_collector


Storage = _StorageClass()
# mccole:/storage


# mccole:traced
def traced(operation_name: str):
    """Decorator that automatically creates spans for functions."""

    def decorator(func: Callable) -> Callable:
        # Get operation name
        op_name = operation_name

        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            # Get current context
            context = Storage.get_context()

            # No tracing, just call function
            if not context:
                return await func(self, *args, **kwargs)

            # Get service name from class
            service_name = getattr(self, "service_name", self.__class__.__name__)

            # Create span
            span = Span(
                trace_id=context.trace_id,
                span_id=generate_id("span_"),
                parent_span_id=context.span_id,
                operation_name=op_name,
                service_name=service_name,
                start_time=self.now,
            )

            # Save old context and set new one
            old_context = Storage.get_context()
            new_context = TraceContext(
                trace_id=context.trace_id,
                span_id=span.span_id,
                parent_span_id=context.span_id,
            )
            Storage.set_context(new_context)

            try:
                # Call function
                result = await func(self, *args, **kwargs)
                span.add_tag("success", True)
                return result

            except Exception as e:
                # Record error
                span.add_tag("error", True)
                span.add_tag("error.message", str(e))
                span.add_log("exception", exception=str(e))
                raise

            finally:
                # Finish span and send to collector
                span.finish(self.now)
                collector = Storage.get_collector()
                if collector:
                    await collector.span_queue.put(span)

                # Restore old context
                Storage.set_context(old_context)

        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            # For sync functions, just add tags but don't trace
            return func(self, *args, **kwargs)

        # Return appropriate wrapper
        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# mccole:/traced


# mccole:trace_root
def trace_root(operation_name: str | None = None):
    """Decorator that creates a new trace with a root span.

    Use this on client methods that initiate requests.
    It handles all the trace ID generation and context setup.

    Usage:
        @trace_root()
        async def make_request(self, req_id):
            # Your request logic here
            # Context is automatically created and set
            pass
    """

    def decorator(func: Callable) -> Callable:
        op_name = operation_name or getattr(func, "__name__", "unknown")

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Get service name
            service_name = getattr(self, "name", self.__class__.__name__)

            # Create new trace
            trace_id = generate_id("trace_")
            root_span_id = generate_id("span_")

            # Create root span
            root_span = Span(
                trace_id=trace_id,
                span_id=root_span_id,
                parent_span_id=None,
                operation_name=f"{service_name}.{op_name}",
                service_name=service_name,
                start_time=self.now,
            )

            # Create and set context
            context = TraceContext(
                trace_id=trace_id,
                span_id=root_span_id,
            )

            # Save old context
            old_context = Storage.get_context()
            Storage.set_context(context)

            try:
                # Call function - it can access context via get_trace_context()
                result = await func(self, *args, **kwargs)
                root_span.add_tag("success", True)
                return result

            except Exception as e:
                # Record error
                root_span.add_tag("error", True)
                root_span.add_tag("error.message", str(e))
                raise

            finally:
                # Finish root span and send to collector
                root_span.finish(self.now)
                collector = Storage.get_collector()
                if collector:
                    await collector.span_queue.put(root_span)

                # Restore old context
                Storage.set_context(old_context)

        return wrapper

    return decorator


# mccole:/trace_root


def add_tag(key: str, value: Any) -> None:
    """Add a tag to the current span.

    This is a convenience function for adding tags within traced functions.
    """
    # Tags would be stored in thread-local span if we tracked that
    # For now, this is a placeholder showing the API
    pass


def add_log(message: str, **fields: Any) -> None:
    """Add a log entry to the current span.

    This is a convenience function for adding logs within traced functions.
    """
    # Logs would be stored in thread-local span if we tracked that
    # For now, this is a placeholder showing the API
    pass
