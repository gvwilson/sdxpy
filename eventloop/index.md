---
title: "An Event Loop"
version: 2
abstract: >
    Libraries like asyncio look like magic, but underneath them is a simple
    idea: a scheduler that runs coroutines one step at a time.
    This chapter builds that scheduler to show how async and await actually work.
syllabus:
-   An async function is a resumable function; calling it returns a coroutine that does nothing until stepped.
-   await is where a task voluntarily hands control back to the scheduler.
-   A coroutine pauses when it awaits and resumes when the thing it awaited is ready.
-   An event loop is a ready queue of tasks, run one await at a time.
-   StopIteration signals that a coroutine has finished.
depends:
-   func
-   protocols
---

Programmers who write networked programs use
Python's `async` and `await` keywords
(or their equivalents in other languages)
to make many tasks appear to run at the same time.
Those keywords look like magic,
but they rest on a simple idea:
a coroutine is a function that can be paused and resumed,
and a scheduler decides which coroutine runs next.

This chapter builds a small version of that scheduler
to show how it works.
[%x concur %] approaches the same problem from the point of view of threads;
here we stay in a single thread and switch between tasks by hand.

## A Resumable Function {: #eventloop-coroutine}

When we call a function defined with `async def`,
Python does not run its body.
Instead it returns a coroutine object
that does nothing until we drive it,
and we drive it by calling its `send` method:

```python
async def hello():
    print("hello")

coro = hello()        # does not print anything yet
coro.send(None)       # now it runs and prints "hello"
```

The first call to `send` must pass `None`.
When the body finishes,
Python raises `StopIteration`,
which is how the driver learns that the coroutine is done.

## An Awaitable {: #eventloop-event}

A coroutine that runs straight from top to bottom is not very useful.
What we want is for a coroutine to pause partway through
and let something else run.
The `await` keyword does exactly this:
it hands control back to whoever called `send`,
along with the object the coroutine is waiting for.

That object must be *awaitable*,
which in Python means it must have an `__await__` method.
The simplest awaitable is an `Event`,
which represents "something that will happen later":

[%inc event.py mark=event %]

The `__await__` method is the whole story.
If the event has not happened yet,
it executes `yield self`,
which pauses the coroutine and hands the event back to the driver.
When the driver sends a value in again,
the method falls through to `return self._value`,
and that value becomes the result of the coroutine's `await` expression.

The `set` method records the event's value
and wakes every task that was waiting for it.
Notice that waking a task just means
putting the task's `step` method back on the scheduler's queue;
the task does not resume right away.

## Driving a Coroutine {: #eventloop-task}

The driver is a class called `Task`.
Its `step` method sends a value into the coroutine
and looks at what comes back out:

[%inc environment.py mark=task %]

If the coroutine has finished,
`send` raises `StopIteration`
and we mark the task as done.
If the coroutine is still running,
`send` returns whatever the coroutine awaited—an `Event`.
The task registers itself as a waiter on that event
and stops,
so that the next task can have a turn.
If the coroutine somehow awaited nothing at all,
we just put the task back on the queue to continue.

## The Loop {: #eventloop-loop}

The last piece is the scheduler itself,
which is nothing more than a queue of work to do:

[%inc environment.py mark=environment %]

`create_task` wraps a coroutine in a `Task`
and schedules its first step.
`run` then repeatedly takes a callback off the front of the queue
and calls it.
When a task awaits an event,
it removes itself from the queue (it is parked on the event);
when the event fires,
it puts the task back.
The loop keeps going until the queue is empty.

To see it all working,
we create two tasks that both wait for the same event:

[%inc demo.py mark=main %]

Running this produces:

```
first: started
second: started
main: both blocked
first: finished
second: finished
```

Both tasks start,
both block on `done`,
and only after `done.set()` do they finish.
There is no parallelism here:
one task runs until it awaits,
then the next task runs until it awaits,
and so on.

## Summary {: #eventloop-summary}

The `async` and `await` keywords are not magic.
A coroutine is a function that can pause and resume;
`await` is a pause point;
and a scheduler is a loop that runs each coroutine until its next pause.
The next chapter ([%x os %]) uses this scheduler
as the kernel of a tiny operating system.

<section class="exercises" markdown="1">
## Exercises {: #eventloop-exercises}

### A Result Event

The `Event` class stores a single value.
Modify it so that a task can await the *same* event multiple times,
receiving the value each time.

### Timeout

Add a `Timeout` event that fires after a delay,
so that a task can write `await env.sleep(5)`.
What new data structure does the scheduler need?

### A Queue

Add a `Queue` that tasks can use to send values to each other,
so that `await queue.get()` blocks until a value is available.

### Interrupting a Task

Add an `interrupt` method that throws an exception into a running task.
When should the task be allowed to catch it?

</section>
