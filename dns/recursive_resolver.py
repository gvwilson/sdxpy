from asimpy import Process, Queue
from dns_message import DNSQuery, DNSResponse, DNSRecord, RecordType
from typing import Optional


# mccole:cacheentry
class CacheEntry:
    """A cached DNS record with expiration time."""

    def __init__(self, record: DNSRecord, expire_time: float):
        self.record = record
        self.expire_time = expire_time

    def is_expired(self, current_time: float) -> bool:
        """Check if this cache entry has expired."""
        return current_time >= self.expire_time
# mccole:/cacheentry


# mccole:resolver_init
class RecursiveDNSResolver(Process):
    """A recursive DNS resolver with caching."""

    def init(
        self,
        name: str,
        request_queue: Queue,
        root_servers: dict[str, Queue],
    ):
        self.name = name
        self.request_queue = request_queue
        self.root_servers = root_servers  # zone -> server queue
        self.cache: dict[tuple[str, RecordType], list[CacheEntry]] = {}
        self.response_queue = Queue(self._env)
        self.queries_received = 0
        self.cache_hits = 0
        self.cache_misses = 0
# mccole:/resolver_init

    # mccole:resolver_run
    async def run(self):
        """Process client DNS queries."""
        while True:
            # Wait for a query from a client
            client_queue, query = await self.request_queue.get()
            self.queries_received += 1

            print(
                f"[{self.now:.3f}] {self.name}: Received query for "
                f"{query.domain} ({query.record_type.value})"
            )

            # Check cache first
            cached_records = self._check_cache(query.domain, query.record_type)

            if cached_records:
                self.cache_hits += 1
                response = DNSResponse(
                    query_id=query.query_id,
                    domain=query.domain,
                    record_type=query.record_type,
                    records=cached_records,
                    authoritative=False,
                    from_cache=True,
                )
                print(f"[{self.now:.3f}] {self.name}: Cache HIT for {query.domain}")
            else:
                self.cache_misses += 1
                print(f"[{self.now:.3f}] {self.name}: Cache MISS for {query.domain}")
                # Recursively resolve
                response = await self._resolve_recursive(query)

                # Cache the results
                if response.records:
                    self._cache_records(response.records)

            # Send response to client
            await client_queue.put(response)
    # mccole:/resolver_run

    # mccole:resolver_cache
    def _check_cache(
        self, domain: str, record_type: RecordType
    ) -> Optional[list[DNSRecord]]:
        """Check if we have a cached record."""
        key = (domain, record_type)
        if key not in self.cache:
            return None

        # Filter out expired entries
        valid_entries = [
            entry for entry in self.cache[key] if not entry.is_expired(self.now)
        ]

        if not valid_entries:
            del self.cache[key]
            return None

        self.cache[key] = valid_entries
        return [entry.record for entry in valid_entries]

    def _cache_records(self, records: list[DNSRecord]):
        """Add records to the cache."""
        for record in records:
            key = (record.name, record.record_type)
            if key not in self.cache:
                self.cache[key] = []

            expire_time = self.now + record.ttl
            self.cache[key].append(CacheEntry(record, expire_time))
    # mccole:/resolver_cache

    # mccole:resolver_resolve
    async def _resolve_recursive(self, query: DNSQuery) -> DNSResponse:
        """Recursively resolve a query by querying authoritative servers."""
        # Find the appropriate authoritative server
        # In real DNS, this involves walking the DNS hierarchy
        # For simplicity, we'll match the longest zone suffix

        matching_zone = None
        for zone in self.root_servers.keys():
            if query.domain.endswith(zone):
                if matching_zone is None or len(zone) > len(matching_zone):
                    matching_zone = zone

        if matching_zone is None:
            # No authoritative server found
            return DNSResponse(
                query_id=query.query_id,
                domain=query.domain,
                record_type=query.record_type,
                records=[],
                authoritative=False,
            )

        # Query the authoritative server
        server_queue = self.root_servers[matching_zone]
        await server_queue.put((self.response_queue, query))

        # Wait for response
        response = await self.response_queue.get()
        return response
    # mccole:/resolver_resolve
