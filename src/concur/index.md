---
title: "Concurrency"
abstract: >
    FIXME
syllabus:
-   FIXME
---

-   `switch.py`: show task switching
-   `parent.py`: show greenlet ID and parentage
-   `classes.py`: use objects instead of bare functions
    -   but `set_other` method is clumsy: how should we connect them?
-   `scheduler.py`: a queue of runnable tasks is the parent of all tasks
-   `catch.py`: show that uncaught exceptions are caught by parent greenlet
    -   error handling is the hardest part of concurrency
-   `inject.py`: pass values into greenlets when resuming them
    -   call to `.run` gets the first value passed in
    -   `.switch` returns a value
    -   exercise: use `.throw` to raise an exception in a greenlet from the outside
-   `resource.py`: busy-wait competition for shared resource
    -   wasteful
-   `wait.py`: resource keeps track of who is waiting and who is ready to run
    -   all scheduling done by the scheduler
    -   if first attempt to acquire fails, acquire again when rescheduled
