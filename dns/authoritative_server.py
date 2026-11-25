from asimpy import Process, Queue
from dns_message import DNSResponse, DNSRecord, RecordType


# mccole:auth_init
class AuthoritativeDNSServer(Process):
    """An authoritative DNS server for a specific zone."""

    def init(self, name: str, zone: str, request_queue: Queue):
        self.name = name
        self.zone = zone  # e.g., "example.com"
        self.request_queue = request_queue
        self.records: dict[tuple[str, RecordType], list[DNSRecord]] = {}
        self.queries_served = 0

    def add_record(self, record: DNSRecord):
        """Add a DNS record to this server's zone."""
        key = (record.name, record.record_type)
        if key not in self.records:
            self.records[key] = []
        self.records[key].append(record)
# mccole:/auth_init

    # mccole:auth_run
    async def run(self):
        """Process DNS queries."""
        while True:
            # Wait for a query
            client_queue, query = await self.request_queue.get()

            # Check if this query is for our zone
            if not query.domain.endswith(self.zone):
                # Not authoritative for this domain
                response = DNSResponse(
                    query_id=query.query_id,
                    domain=query.domain,
                    record_type=query.record_type,
                    records=[],
                    authoritative=False,
                )
            else:
                # Look up the record
                key = (query.domain, query.record_type)
                records = self.records.get(key, [])

                # Handle CNAME (alias) records
                if not records and query.record_type == RecordType.A:
                    cname_key = (query.domain, RecordType.CNAME)
                    cname_records = self.records.get(cname_key, [])
                    if cname_records:
                        # Follow the CNAME
                        canonical_name = cname_records[0].value
                        a_key = (canonical_name, RecordType.A)
                        records = self.records.get(a_key, [])
                        records = cname_records + records

                response = DNSResponse(
                    query_id=query.query_id,
                    domain=query.domain,
                    record_type=query.record_type,
                    records=records,
                    authoritative=True,
                )

            print(
                f"[{self.now:.3f}] {self.name}: Query for {query.domain} "
                f"({query.record_type.value}) -> {len(response.records)} record(s)"
            )

            # Simulate processing delay
            await self.timeout(0.01)

            # Send response
            await client_queue.put(response)
            self.queries_served += 1
    # mccole:/auth_run
