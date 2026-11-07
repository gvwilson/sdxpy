from environment import Environment
from event import Event


# mccole:sample
def test_await_blocks_until_set():
    env = Environment()
    ev = Event(env)
    seen = []

    async def task():
        seen.append(await ev)

    env.create_task(task())
    env.run()
    assert seen == []  # still blocked

    ev.set(7)
    env.run()
    assert seen == [7]
# mccole:/sample


def test_set_before_await_returns_value():
    env = Environment()
    ev = Event(env)
    ev.set(42)
    seen = []

    async def task():
        seen.append(await ev)

    env.create_task(task())
    env.run()
    assert seen == [42]
