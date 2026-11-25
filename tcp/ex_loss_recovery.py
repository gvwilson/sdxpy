"""TCP demonstration under extreme packet loss conditions."""

from asimpy import Environment
from unreliable_network import UnreliableNetwork
from tcp_connection import TCPConnection
from tcp_applications import TCPClient, TCPServer
from dsdx import dsdx


# mccole:highlossexample
def main():
    env = Environment()

    print("## High Loss TCP Scenario")
    print("Testing TCP robustness with extreme conditions:")
    print("  - 40% packet loss (!!)")
    print("  - 20% packet reordering")
    print("  - 10% packet duplication")
    print("  - Larger message requiring multiple segments")

    # Extremely unreliable network
    network = UnreliableNetwork(
        env,
        loss_rate=0.40,  # 40% packet loss!
        reorder_rate=0.20,  # 20% reordering
        duplicate_rate=0.10,  # 10% duplication
        delay_range=(0.2, 0.6),
    )

    # TCP with aggressive retransmission
    server_conn = TCPConnection(
        env,
        "10.0.0.1",
        5000,
        network,
        window_size=3,
        timeout=1.0,  # Faster retransmit
    )

    client_conn = TCPConnection(
        env, "10.0.0.2", 6000, network, window_size=3, timeout=1.0
    )

    # Create applications
    TCPServer(env, server_conn)

    # Transfer larger message that will require multiple segments
    message = (
        "This is a much longer message that will be split into multiple "
        "TCP segments. Despite 40% packet loss - which is extremely high - "
        "TCP will successfully deliver every byte through retransmission. "
        "You'll see many timeouts and retransmissions, but eventually "
        "the complete message arrives in perfect order. "
    ) * 5  # Repeat 5 times

    TCPClient(env, client_conn, "10.0.0.1", 5000, message)

    # Run simulation (longer time for high loss)
    env.run(until=40)

    # Print statistics
    network.print_statistics()
    client_conn.print_statistics()
    server_conn.print_statistics()

    # Verify delivery
    print("## Verification:")
    expected_bytes = len(message.encode("utf-8"))
    if server_conn.bytes_received == expected_bytes:
        print(f"Success: All {expected_bytes} bytes delivered correctly!")
    else:
        print(f"Incomplete: {server_conn.bytes_received}/{expected_bytes} bytes")
# mccole:/highlossexample


if __name__ == "__main__":
    dsdx(main)
