from device import Queue
from environment import Environment


# mccole:sample
def test_get_blocks_until_put():
    env = Environment()
    device = Queue(env)
    seen = []

    async def consumer():
        seen.append(await device.get())

    env.create_process("consumer", consumer())
    env.run()
    assert seen == []  # still blocked, queue is empty

    device.put(42)
    env.run()
    assert seen == [42]
# mccole:/sample


def test_put_buffers_when_no_getter():
    env = Environment()
    device = Queue(env)
    seen = []

    async def consumer():
        seen.append(await device.get())

    device.put(1)
    device.put(2)
    env.create_process("consumer", consumer())
    env.run()
    assert seen == [1]
