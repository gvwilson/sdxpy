from greenlet import getcurrent, greenlet


def first_func():
    current = getcurrent()
    print(f"=> first:\n..current {current}\n..parent {current.parent}")
    second_task.switch()
    print("=> first")
    return "finished"


def second_func():
    current = getcurrent()
    print(f"=> second:\n..current {current}\n..parent {current.parent}")
    first_task.switch()
    print("whoops")


print(f"main {getcurrent()}")
first_task = greenlet(first_func)
second_task = greenlet(second_func)
result = first_task.switch()
print(result)
print(f"first_task: {first_task}")
print(f"second_task: {second_task}")
