from asimpy import Environment, Queue
from authoritative_server import AuthoritativeDNSServer
from recursive_resolver import RecursiveDNSResolver
from dns_client import DNSClient
from dns_message import DNSRecord, RecordType
from dsdx import dsdx


# mccole:loadclient
class LoadTestClient(DNSClient):
    """Client that generates load to demonstrate caching benefits."""

    def init(self, name: str, resolver_queue: Queue, domains: list[str] | None = None):
        super().init(name, resolver_queue)
        self.domains = [] if domains is None else domains

    async def run(self):
        """Repeatedly lookup domains."""
        for i in range(10):
            # Lookup each domain
            for domain in self.domains:
                await self.lookup(domain)
                await self.timeout(0.5)

            # Wait before next round
            await self.timeout(2.0)
# mccole:/loadclient


# mccole:hierarchy
def main():
    """Demonstrate DNS hierarchy and caching benefits."""
    env = Environment()

    # Create root DNS server
    root_queue = Queue(env)
    root_server = AuthoritativeDNSServer(env, "root.dns", ".", root_queue)

    # Add NS records pointing to TLD servers
    root_server.add_record(DNSRecord("com", RecordType.NS, "tld.com.dns", ttl=86400))
    root_server.add_record(DNSRecord("org", RecordType.NS, "tld.org.dns", ttl=86400))

    # Create TLD server for .com
    com_queue = Queue(env)
    com_server = AuthoritativeDNSServer(env, "tld.com.dns", "com", com_queue)
    com_server.add_record(
        DNSRecord("example.com", RecordType.NS, "ns1.example.com", ttl=86400)
    )

    # Create authoritative server for example.com
    example_queue = Queue(env)
    example_server = AuthoritativeDNSServer(
        env, "ns1.example.com", "example.com", example_queue
    )
    example_server.add_record(
        DNSRecord("www.example.com", RecordType.A, "192.0.2.1", ttl=60)
    )
    example_server.add_record(
        DNSRecord("api.example.com", RecordType.A, "192.0.2.10", ttl=60)
    )
    example_server.add_record(
        DNSRecord("cdn.example.com", RecordType.A, "192.0.2.20", ttl=60)
    )

    # Create TLD server for .org
    org_queue = Queue(env)
    org_server = AuthoritativeDNSServer(env, "tld.org.dns", "org", org_queue)
    org_server.add_record(
        DNSRecord("another.org", RecordType.NS, "ns1.another.org", ttl=86400)
    )

    # Create authoritative server for another.org
    another_queue = Queue(env)
    another_server = AuthoritativeDNSServer(
        env, "ns1.another.org", "another.org", another_queue
    )
    another_server.add_record(
        DNSRecord("www.another.org", RecordType.A, "198.51.100.1", ttl=60)
    )

    # Create multiple recursive resolvers (like ISP DNS servers)
    resolver1_queue = Queue(env)
    resolver1 = RecursiveDNSResolver(
        env,
        "resolver1.isp.net",
        resolver1_queue,
        root_servers={
            "example.com": example_queue,
            "another.org": another_queue,
        },
    )

    resolver2_queue = Queue(env)
    resolver2 = RecursiveDNSResolver(
        env,
        "resolver2.isp.net",
        resolver2_queue,
        root_servers={
            "example.com": example_queue,
            "another.org": another_queue,
        },
    )

    # Create clients using different resolvers
    LoadTestClient(
        env,
        "client1",
        resolver1_queue,
        domains=["www.example.com", "api.example.com"],
    )

    LoadTestClient(
        env,
        "client2",
        resolver1_queue,
        domains=["www.example.com", "cdn.example.com"],
    )

    LoadTestClient(env, "client3", resolver2_queue, domains=["www.another.org"])

    # Run simulation
    env.run(until=50)

    # Print statistics
    print("\n=== DNS Hierarchy Statistics ===")
    print("\nAuthoritative Servers:")
    print(f"  example.com: {example_server.queries_served} queries")
    print(f"  another.org: {another_server.queries_served} queries")

    print("\nResolver 1:")
    print(f"  Total queries: {resolver1.queries_received}")
    print(f"  Cache hits: {resolver1.cache_hits}")
    print(f"  Cache misses: {resolver1.cache_misses}")
    if resolver1.queries_received > 0:
        print(
            f"  Cache hit rate: {(resolver1.cache_hits / resolver1.queries_received) * 100:.1f}%"
        )

    print("\nResolver 2:")
    print(f"  Total queries: {resolver2.queries_received}")
    print(f"  Cache hits: {resolver2.cache_hits}")
    print(f"  Cache misses: {resolver2.cache_misses}")
    if resolver2.queries_received > 0:
        print(
            f"  Cache hit rate: {(resolver2.cache_hits / resolver2.queries_received) * 100:.1f}%"
        )

    print(
        f"\nTotal authoritative queries: {example_server.queries_served + another_server.queries_served}"
    )
    print(
        f"Total client queries: {resolver1.queries_received + resolver2.queries_received}"
    )
    print(
        f"Query reduction from caching: {(1 - (example_server.queries_served + another_server.queries_served) / (resolver1.queries_received + resolver2.queries_received)) * 100:.1f}%"
    )
# mccole:/hierarchy


if __name__ == "__main__":
    dsdx(main)
