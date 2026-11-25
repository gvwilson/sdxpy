from asimpy import Environment, Queue
from authoritative_server import AuthoritativeDNSServer
from recursive_resolver import RecursiveDNSResolver
from dns_client import DNSClient
from dns_message import DNSRecord, RecordType
from dsdx import dsdx


# mccole:testclient
class TestClient(DNSClient):
    """Test client that performs a series of lookups."""

    async def run(self):
        """Perform test lookups."""
        # Lookup example.com
        await self.lookup("www.example.com")
        await self.timeout(1.0)

        # Lookup again - should be cached
        await self.lookup("www.example.com")
        await self.timeout(1.0)

        # Lookup different domain
        await self.lookup("mail.example.com")
        await self.timeout(1.0)

        # Lookup from different zone
        await self.lookup("www.another.org")
# mccole:/testclient


# mccole:simulate
def main():
    """Simulate DNS resolution with caching."""
    env = Environment()

    # Create authoritative servers for different zones
    example_queue = Queue(env)
    example_server = AuthoritativeDNSServer(
        env, "ns1.example.com", "example.com", example_queue
    )

    # Add records to example.com zone
    example_server.add_record(
        DNSRecord("www.example.com", RecordType.A, "192.0.2.1", ttl=300)
    )
    example_server.add_record(
        DNSRecord("mail.example.com", RecordType.A, "192.0.2.2", ttl=300)
    )
    example_server.add_record(
        DNSRecord("ftp.example.com", RecordType.CNAME, "www.example.com", ttl=300)
    )

    # Create authoritative server for another.org
    another_queue = Queue(env)
    another_server = AuthoritativeDNSServer(
        env, "ns1.another.org", "another.org", another_queue
    )
    another_server.add_record(
        DNSRecord("www.another.org", RecordType.A, "198.51.100.1", ttl=300)
    )

    # Create recursive resolver
    resolver_queue = Queue(env)
    resolver = RecursiveDNSResolver(
        env,
        "resolver.isp.net",
        resolver_queue,
        root_servers={"example.com": example_queue, "another.org": another_queue},
    )

    # Create test clients
    TestClient(env, "client1.local", resolver_queue)

    # Run simulation
    env.run(until=10)

    # Print statistics
    print("\n=== DNS Resolution Statistics ===")
    print(f"Example.com server: {example_server.queries_served} queries")
    print(f"Another.org server: {another_server.queries_served} queries")
    print("\nResolver:")
    print(f"  Total queries: {resolver.queries_received}")
    print(f"  Cache hits: {resolver.cache_hits}")
    print(f"  Cache misses: {resolver.cache_misses}")
    if resolver.queries_received > 0:
        hit_rate = (resolver.cache_hits / resolver.queries_received) * 100
        print(f"  Cache hit rate: {hit_rate:.1f}%")
# mccole:/simulate


if __name__ == "__main__":
    dsdx(main)
