"""Example using JSON trace collector."""

from asimpy import Environment, Process, Queue
from json_collector import JSONTraceCollector
from simple_service import SimpleService
from tracing_decorators import Storage, trace_root
from tracing_types import BaseCollector, ServiceRequest
from dsdx import dsdx


# mccole:client
class SimpleClient(Process):
    """Client that initiates traced requests."""

    def init(self, name: str, service: SimpleService, collector: BaseCollector):
        self.name = name
        self.service = service
        self.collector = collector
        Storage.set_collector(collector)

    async def run(self) -> None:
        """Generate requests."""
        for i in range(2):
            await self.timeout(1.5)
            await self.make_request(f"req_{i + 1}")

    @trace_root("make_request")
    async def make_request(self, req_id: str) -> None:
        """Make a traced request - decorator handles trace creation."""
        context = Storage.get_context()

        response_queue = Queue(self._env)
        request = ServiceRequest(
            request_id=req_id,
            context=context,
            payload={"data": f"request_{req_id}"},
            response_queue=response_queue,
        )

        await self.service.request_queue.put(request)
        response = await response_queue.get()

        return response
# mccole:/client


# mccole:demo
def main() -> None:
    """Demonstrate JSON-formatted tracing output."""
    env = Environment()
    collector = JSONTraceCollector(env)
    service = SimpleService(env, "OrderService", collector, verbose=False)
    SimpleClient(env, "Client", service, collector)
    env.run(until=4)
# mccole:/demo


if __name__ == "__main__":
    dsdx(main)
