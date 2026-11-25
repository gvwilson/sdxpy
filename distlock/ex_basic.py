"""Simulate multiple clients competing for a lock."""
from asimpy import Environment
from basic_lock_server import LockServer
from lock_client import LockClient
from dsdx import dsdx


# mccole:basicexample
def main():
    env = Environment()

    # Create lock server
    server = LockServer(env, "Server1", lease_duration=5.0)

    # Create clients that want the same resource
    LockClient(env, "Client1", server, "database", work_duration=3.0)
    LockClient(env, "Client2", server, "database", work_duration=2.0)
    LockClient(env, "Client3", server, "database", work_duration=4.0)

    env.run(until=20)
# mccole:/basicexample


if __name__ == "__main__":
    dsdx(main)
