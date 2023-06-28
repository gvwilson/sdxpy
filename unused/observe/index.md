-   `pull_buggy.py`
    -   doesn't update C because A->B->D and then C thinks D wasn't out of date
    -   so switch to push notifications

-   `push_simple.py`: observables push notifications, execution is immediate

-   `push_origin.py`: keep track of originator to avoid cycles
    -   use UUID as identifier in exercise

-   `push_queue.py`: use the graph to add work to a queue for execution
