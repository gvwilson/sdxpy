from environment import Environment
from event import Event


def main():
    env = Environment()
    done = Event(env)

    async def first():
        env.log("first", "started")
        await done
        env.log("first", "finished")

    async def second():
        env.log("second", "started")
        await done
        env.log("second", "finished")

    env.create_task(first())
    env.create_task(second())
    env.run()
    env.log("main", "both blocked")

    done.set()
    env.run()

    for name, message in env.get_log():
        print(f"{name}: {message}")


if __name__ == "__main__":
    main()
