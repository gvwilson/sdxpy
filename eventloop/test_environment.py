from environment import Environment
from event import Event


# mccole:sample
def test_tasks_block_and_resume_in_order():
    env = Environment()
    tick = Event(env)
    log = []

    async def a():
        log.append("a1")
        await tick
        log.append("a2")

    async def b():
        log.append("b1")
        await tick
        log.append("b2")

    env.create_task(a())
    env.create_task(b())
    env.run()
    assert log == ["a1", "b1"]

    tick.set()
    env.run()
    assert log == ["a1", "b1", "a2", "b2"]
# mccole:/sample


def test_task_runs_to_completion():
    env = Environment()
    log = []

    async def task():
        log.append("run")

    env.create_task(task())
    env.run()
    assert log == ["run"]
