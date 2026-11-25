"""Hierarchical DNS resolver that walks the delegation chain.

Unlike the simplified resolver (which jumps directly to an authoritative server),
this resolver starts at a root server and follows NS referrals down the hierarchy,
just as real DNS resolvers do.
"""

from asimpy import Process, Queue
from dns_message import DNSQuery, DNSResponse, DNSRecord, RecordType
from recursive_resolver import CacheEntry
from typing import Optional


# mccole:hier_init
class HierarchicalResolver(Process):
    """Recursive resolver that walks the hierarchy from root servers.

    The resolver starts every query at a root server.
    When a server returns an NS referral (the zone is delegated to another
    server), the resolver follows the referral.  This continues until it
    reaches an authoritative server that can answer the query directly.
    """

    def init(
        self,
        name: str,
        request_queue: Queue,
        root_server_queue: Queue,
    ):
        self.name = name
        self.request_queue = request_queue
        # The single entry point into the hierarchy.
        self.root_server_queue = root_server_queue
        self.response_queue: Queue = Queue(self._env)

        self.cache: dict[tuple[str, RecordType], list[CacheEntry]] = {}
        self.queries_received = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.referrals_followed = 0
# mccole:/hier_init

    # mccole:hier_run
    async def run(self) -> None:
        """Process client DNS queries."""
        while True:
            client_queue, query = await self.request_queue.get()
            self.queries_received += 1

            print(
                f"[{self.now:.3f}] {self.name}: Query for "
                f"{query.domain} ({query.record_type.value})"
            )

            cached = self._check_cache(query.domain, query.record_type)
            if cached:
                self.cache_hits += 1
                print(f"[{self.now:.3f}] {self.name}: Cache HIT for {query.domain}")
                response = DNSResponse(
                    query_id=query.query_id,
                    domain=query.domain,
                    record_type=query.record_type,
                    records=cached,
                    authoritative=False,
                    from_cache=True,
                )
            else:
                self.cache_misses += 1
                print(
                    f"[{self.now:.3f}] {self.name}: "
                    f"Cache MISS — starting hierarchy walk for {query.domain}"
                )
                response = await self._walk_hierarchy(query)
                if response.records:
                    self._cache_records(response.records)
                # Cache negative responses to avoid hammering servers for
                # non-existent domains.
                elif not response.records:
                    self._cache_negative(query.domain, query.record_type)

            await client_queue.put(response)
    # mccole:/hier_run

    # mccole:hier_walk
    async def _walk_hierarchy(self, query: DNSQuery) -> DNSResponse:
        """Walk the DNS delegation hierarchy from root to authoritative server.

        The algorithm:
        1. Start at the root server.
        2. Send the query.
        3. If the response is authoritative, return it.
        4. If the response is a referral (NS records), follow the first referral
           by looking up the referred zone's server and repeating from step 2.
        5. If neither, return a not-found response.

        In real DNS the resolver must also resolve the IP address of the
        referred name server (a glue record lookup) if it is not already known.
        We simulate this by giving each server a reference to the next layer.
        """
        current_server_queue = self.root_server_queue
        labels = query.domain.split(".")

        # Walk up to len(labels) levels of delegation.
        for depth in range(len(labels) + 1):
            await current_server_queue.put((self.response_queue, query))
            response = await self.response_queue.get()

            if response.authoritative:
                # We reached an authoritative server.
                return response

            # Look for NS referrals in the response.
            ns_records = [r for r in response.records if r.record_type == RecordType.NS]
            if ns_records:
                # The NS record's value is the queue for the delegated zone server.
                # In real DNS, NS values are hostnames that must be resolved
                # to IP addresses; here we use the hostname as a direct key
                # into the resolver's known server map.
                referred_zone = ns_records[0].value
                next_queue = self._known_servers.get(referred_zone)
                if next_queue is None:
                    print(
                        f"[{self.now:.3f}] {self.name}: "
                        f"Unknown referral target {referred_zone}"
                    )
                    break
                self.referrals_followed += 1
                current_server_queue = next_queue
                print(
                    f"[{self.now:.3f}] {self.name}: "
                    f"Following referral to {referred_zone} (depth {depth + 1})"
                )
            else:
                # No answer, no referral.
                break

        return DNSResponse(
            query_id=query.query_id,
            domain=query.domain,
            record_type=query.record_type,
            records=[],
            authoritative=False,
        )

    def register_server(self, zone: str, server_queue: Queue) -> None:
        """Register the queue for a delegated zone's server."""
        if not hasattr(self, "_known_servers"):
            self._known_servers: dict[str, Queue] = {}
        self._known_servers[zone] = server_queue
    # mccole:/hier_walk

    # mccole:hier_negative
    def _cache_negative(self, domain: str, record_type: RecordType) -> None:
        """Cache a negative response (NXDOMAIN) to reduce redundant queries.

        Negative caching prevents the resolver from querying the authoritative
        server again for a domain that does not exist.  The TTL for negative
        responses is typically found in the SOA record of the authoritative
        zone; we use a fixed value here.
        """
        NEGATIVE_TTL = 300  # 5 minutes, a common default
        key = (domain, record_type)
        # Store an empty entry list with an expiry.  _check_cache returns None
        # for an empty list, so we store a sentinel entry instead.
        sentinel = DNSRecord(
            name=domain,
            value="NXDOMAIN",
            record_type=record_type,
            ttl=NEGATIVE_TTL,
        )
        entry = CacheEntry(sentinel, self.now + NEGATIVE_TTL)
        self.cache[key] = [entry]
        print(
            f"[{self.now:.3f}] {self.name}: "
            f"Cached NXDOMAIN for {domain} (TTL {NEGATIVE_TTL}s)"
        )

    def _is_negative_entry(self, record: DNSRecord) -> bool:
        """Return True if this is a negative-cache sentinel record."""
        return record.value == "NXDOMAIN"
    # mccole:/hier_negative

    def _check_cache(
        self, domain: str, record_type: RecordType
    ) -> Optional[list[DNSRecord]]:
        key = (domain, record_type)
        if key not in self.cache:
            return None
        valid = [e for e in self.cache[key] if not e.is_expired(self.now)]
        if not valid:
            del self.cache[key]
            return None
        self.cache[key] = valid
        records = [e.record for e in valid]
        # Filter out negative-cache sentinels so callers get an empty list.
        real_records = [r for r in records if not self._is_negative_entry(r)]
        if real_records:
            return real_records
        # All entries are negative sentinels: domain does not exist.
        return []

    def _cache_records(self, records: list[DNSRecord]) -> None:
        for record in records:
            key = (record.name, record.record_type)
            if key not in self.cache:
                self.cache[key] = []
            self.cache[key].append(CacheEntry(record, self.now + record.ttl))
