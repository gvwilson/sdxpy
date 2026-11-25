"""Demonstrate replicated lock manager."""

from asimpy import Environment
from replicated_lock_manager import ReplicatedLockManager
from replicated_lock_client import ReplicatedLockClient
from dsdx import dsdx


# mccole:replicatedexample
def main():
    env = Environment()

    # Create manager with 3 servers
    manager = ReplicatedLockManager(env, num_servers=3, lease_duration=5.0)

    # Create competing clients
    ReplicatedLockClient(env, "Client1", manager, "resource", 3.0)
    ReplicatedLockClient(env, "Client2", manager, "resource", 2.0, initial_delay=2.0)

    env.run(until=15)
# mccole:/replicatedexample


if __name__ == "__main__":
    dsdx(main)
