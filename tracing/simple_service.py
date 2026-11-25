"""Simple service instrumented with tracing decorators."""

import random
from asimpy import Process, Queue
from tracing_types import ServiceRequest, ServiceResponse
from tracing_decorators import Storage, traced


# mccole:simple
class SimpleService(Process):
    """Service instrumented with decorators."""

    def init(self, service_name: str, collector, verbose: bool = True):
        self.service_name = service_name
        self.collector = collector
        self.verbose = verbose
        self.request_queue = Queue(self._env)

        # Set collector for decorators
        Storage.set_collector(collector)

        if self.verbose:
            print(f"[{self.now:.1f}] {self.service_name} started")

    async def run(self) -> None:
        """Handle incoming requests."""
        while True:
            request = await self.request_queue.get()
            await self.handle_request(request)

    @traced("handle_request")
    async def handle_request(self, request: ServiceRequest) -> None:
        """Handle request - automatically traced."""
        if self.verbose:
            print(f"[{self.now:.1f}] {self.service_name}: Processing {request}")

        # Set context for nested calls
        Storage.set_context(request.context)

        # Simulate processing
        await self.timeout(random.uniform(0.1, 0.3))

        # Do some work
        data = await self.process_data(request.payload)

        # Send response
        await request.response_queue.put(
            ServiceResponse(request_id=request.request_id, success=True, data=data)
        )

    @traced("process_data")
    async def process_data(self, payload: dict) -> dict:
        """Process data - automatically traced as child span."""
        await self.timeout(random.uniform(0.05, 0.15))
        return {"processed": True, "input": payload}


# mccole:/simple
