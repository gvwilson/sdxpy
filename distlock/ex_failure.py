"""Demonstrate lease expiration after client failure."""

from asimpy import Environment
from basic_lock_server import LockServer
from lock_client import LockClient
from failing_client import FailingClient
from dsdx import dsdx


# mccole:failureexample
def main():
    env = Environment()

    server = LockServer(env, "Server1", lease_duration=3.0)

    # Client that will crash
    FailingClient(
        env, "FailClient", server, "database", work_duration=10.0, fail_after=1.0
    )

    # Client that waits and then tries to acquire
    LockClient(env, "Client2", server, "database", work_duration=2.0, initial_delay=5.0)

    env.run(until=15)
# mccole:/failureexample


if __name__ == "__main__":
    dsdx(main)
