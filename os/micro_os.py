from device import Queue
from environment import Environment


# mccole:main
def main():
    env = Environment()
    device = Queue(env)

    async def producer():
        for word in ["hello", "world"]:
            await env.sleep(1)
            env.log("producer", f"writing {word}")
            await device.put(word)
        await device.put(None)  # sentinel to stop the consumer

    async def consumer():
        while True:
            env.log("consumer", "waiting")
            item = await device.get()
            if item is None:
                break
            env.log("consumer", f"got {item}")

    env.create_process("producer", producer())
    env.create_process("consumer", consumer())
    env.run()

    for time, name, message in env.get_log():
        print(f"{time:2} {name}: {message}")
# mccole:/main


if __name__ == "__main__":
    main()
