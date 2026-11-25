from tracing_types import Span


def generate_id(prefix):
    return prefix


class GenericService:
    def __init__(self):
        self.service_name = "service name"
        self.now = 0

    async def do_work(self):
        pass


# mccole:service
class Service(GenericService):
    async def handle_request(self, request):
        # Create span manually
        span = Span(
            trace_id=request.context.trace_id,
            span_id=generate_id("span_"),
            parent_span_id=request.context.span_id,
            operation_name="handle_request",
            service_name=self.service_name,
            start_time=self.now,
        )

        try:
            # Do work
            result = await self.do_work()
            span.add_tag("success", True)
            return result

        except Exception:
            # Handle error
            span.add_tag("error", True)
            raise

        finally:
            # Finish and send span
            span.finish(self.now)
            await self.collector.span_queue.put(span)


# mccole:/service
