from greenlet import greenlet


def first_func():
    print("=> first")
    second_task.switch()
    print("=> first")
    return "finished"


def second_func():
    print("=> second")
    first_task.switch()
    print("whoops")


first_task = greenlet(first_func)
second_task = greenlet(second_func)
result = first_task.switch()
print(result)
