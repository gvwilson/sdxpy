from asimpy import Environment, Queue
from ntp_server import NTPServer
from ntp_client import NTPClient
from dsdx import dsdx


# mccole:simulate
def main():
    """Simulate NTP clock synchronization."""
    env = Environment()

    # Create server queue
    server_queue = Queue(env)

    # Create NTP server (stratum 1 - connected to reference clock)
    server = NTPServer(env, "time.example.com", stratum=1, request_queue=server_queue)

    # Create clients with different initial clock offsets
    client1 = NTPClient(
        env,
        "client1.local",
        server_queue,
        sync_interval=5.0,
        initial_offset=2.5,  # 2.5 seconds fast
    )

    client2 = NTPClient(
        env,
        "client2.local",
        server_queue,
        sync_interval=5.0,
        initial_offset=-1.8,  # 1.8 seconds slow
    )

    client3 = NTPClient(
        env,
        "client3.local",
        server_queue,
        sync_interval=7.0,
        initial_offset=0.5,  # 0.5 seconds fast
    )

    # Run simulation
    env.run(until=25)

    # Print statistics
    print("\n=== NTP Synchronization Statistics ===")
    print(f"Server requests served: {server.requests_served}")

    for client in [client1, client2, client3]:
        print(f"\n{client.name}:")
        print(f"  Syncs performed: {client.syncs_performed}")
        print(f"  Final clock offset: {client.clock_offset:.6f}s")
        if client.offset_history:
            print(
                f"  Average correction: {sum(client.offset_history) / len(client.offset_history):.6f}s"
            )
# mccole:/simulate


if __name__ == "__main__":
    dsdx(main)
