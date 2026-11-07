from environment import Environment


# mccole:sample
def test_sleep_advances_clock():
    env = Environment()
    log = []

    async def sleeper():
        log.append((env.now, "before"))
        await env.sleep(5)
        log.append((env.now, "after"))

    env.create_process("sleeper", sleeper())
    env.run()
    assert log == [(0, "before"), (5, "after")]
    assert env.now == 5
# mccole:/sample
