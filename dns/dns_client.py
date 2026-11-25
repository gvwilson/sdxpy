from asimpy import Process, Queue
from dns_message import DNSQuery, RecordType


# mccole:client_init
class DNSClient(Process):
    """A DNS client that performs lookups."""

    def init(self, name: str, resolver_queue: Queue):
        self.name = name
        self.resolver_queue = resolver_queue
        self.response_queue = Queue(self._env)
        self.query_counter = 0
        self.queries_sent = 0

    async def run(self):
        """Override in subclass to perform lookups."""
        pass
# mccole:/client_init

    # mccole:client_lookup
    async def lookup(self, domain: str, record_type: RecordType = RecordType.A):
        """Perform a DNS lookup."""
        self.query_counter += 1
        query = DNSQuery(
            query_id=self.query_counter, domain=domain, record_type=record_type
        )

        print(
            f"[{self.now:.3f}] {self.name}: Looking up {domain} ({record_type.value})"
        )

        # Send query to resolver
        await self.resolver_queue.put((self.response_queue, query))
        self.queries_sent += 1

        # Wait for response
        response = await self.response_queue.get()

        # Print results
        if response.records:
            cache_status = " (cached)" if response.from_cache else ""
            print(f"[{self.now:.3f}] {self.name}: Resolved {domain}{cache_status}:")
            for record in response.records:
                print(f"  {record.name} -> {record.value} (TTL: {record.ttl}s)")
        else:
            print(f"[{self.now:.3f}] {self.name}: No records found for {domain}")

        return response
    # mccole:/client_lookup
