---
title: "Observers"
abstract: >
    FIXME
syllabus:
-   FIXME
---

-   `push_simple.py`: observables push notifications, execution is immediate
-   `push_buggy.py`: infinite recursion
-   `push_origin.py`: keep track of originator to avoid cycles
    -   use UUID as identifier in exercise
-   `push_queue.py`: use the graph to add work to a queue for execution
-   `delay_queue.py`: split action from notification
-   `delay_queue_verbose.py`: run with tracing
-   `logging.py`: queue records actions and causes (better than verbose flag)
