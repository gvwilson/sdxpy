---
title: "A Micro-Operating System"
version: 2
abstract: >
    An operating system is, at heart, a scheduler that runs processes
    and lets them block when they need to wait for input or output.
    This chapter builds a tiny operating system on top of the event loop
    from the previous chapter.
syllabus:
-   A process is a coroutine plus the state the kernel tracks for it.
-   A process blocks on input or output by awaiting an event.
-   A timer lets a process sleep for a fixed number of simulated time units.
-   A device is a queue that processes put data into and get data out of.
-   The kernel is a ready queue plus a clock that advances to the next scheduled event.
depends:
-   eventloop
---

An operating system has two jobs.
The first is to run many programs,
switching between them so quickly that they all appear to run at once.
The second is to let those programs wait for input and output
without wasting the processor.

In [%x eventloop %] we built the first half:
a scheduler that runs coroutines one step at a time.
This chapter builds the second half,
turning that scheduler into a tiny operating system.
There is no virtual memory and no protection;
there are just processes that run, block, and are woken up again.

## The Kernel and Its Clock {: #os-kernel}

The scheduler from [%x eventloop %] had no sense of time.
An operating system needs a clock
so that a process can ask to be woken up later.
Our kernel therefore adds a simulated clock
and a `sleep` method:

[%inc environment.py mark=environment %]

`schedule` puts a callback on the ready queue to run immediately.
`schedule_at` puts a callback on a heap keyed by the time it should run.
`run` drains the ready queue first,
then advances the clock to the next scheduled time
and runs that callback.

A process sleeps by awaiting a `Timeout`:

[%inc environment.py mark=timeout %]

A `Timeout` is just an `Event`
that schedules its own `set` call for a future time.
The `Event` itself is unchanged from [%x eventloop %]:

[%inc environment.py mark=event %]

## Processes {: #os-process}

A process is a coroutine with a name,
plus the `step` method that the kernel uses to drive it.
This is the `Task` class from [%x eventloop %],
renamed to make its role clear:

[%inc environment.py mark=process %]

When a process awaits an event,
it is removed from the ready queue.
The kernel does not track *why* it stopped:
it only knows that the process will be put back
when some event fires.
That is the essence of a process:
a piece of work that runs until it cannot make progress,
then waits.

## A Device {: #os-device}

Processes usually block because they are waiting for a device.
A keyboard produces input when a key is pressed;
a network card produces input when a packet arrives.
We can model all such devices with a queue:

[%inc device.py mark=queue %]

`get` returns the next available item,
or a pending event if the device is empty.
`put` hands an item directly to a waiting process,
or buffers it if nobody is waiting.
A process that wants input simply writes:

```python
item = await device.get()
```

If the device is empty,
the process is parked until another process puts something in.

## Putting It Together {: #os-demo}

To see the whole operating system at work,
we create two processes:
a producer that writes words to a device,
and a consumer that blocks reading from it:

[%inc micro_os.py mark=main %]

Running this produces:

```
 0 consumer: waiting
 1 producer: writing hello
 1 consumer: got hello
 1 consumer: waiting
 2 producer: writing world
 2 consumer: got world
 2 consumer: waiting
```

The producer sleeps for one time unit before each write.
The consumer wakes at time 0, finds the device empty, and blocks.
At time 1 the producer writes `hello`,
which wakes the consumer,
which reads the word and blocks again.
The two processes take turns running,
even though there is only one processor.

## Summary {: #os-summary}

An operating system is a scheduler with a clock
and a set of devices that processes can block on.
A process is a coroutine;
blocking is an `await`;
and a device is a queue that delivers values
from a producer to a consumer.

<section class="exercises" markdown="1">
## Exercises {: #os-exercises}

### Multiple Producers

Add a second producer that writes its own words,
and show that the consumer receives a valid interleaving.
How does the order depend on the sleep delays?

### A Lock

Add a `Resource` with an `acquire` method,
so that a process can wait for exclusive access to a device.

### Bounded Devices

Modify `Queue` to have a maximum capacity,
so that `put` blocks when the device is full.

### Process States

Add a `state` attribute to `Process`
that is `"running"`, `"ready"`, or `"blocked"`,
and update it as the process moves between those states.

### A Scheduling Policy

The kernel always runs the process that has been waiting the longest.
Add a priority so that some processes run before others.

</section>
