from greenlet import greenlet


def func_a():
    print("=> A")
    task_b.switch()
    print("=> A")
    return "finished"


def func_b():
    print("=> B")
    task_a.switch()
    print("whoops")


task_a = greenlet(func_a)
task_b = greenlet(func_b)
result = task_a.switch()
print(result)
