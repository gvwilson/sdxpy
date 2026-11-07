---
title: "An Event Loop"
---

<section class="slide" markdown="1">

## Overview

-   `async` and `await` look like magic

-   Underneath: a coroutine is a resumable function

-   A scheduler decides which coroutine runs next

</section>
<section class="slide" markdown="1">

## Resumable Functions

-   `async def` returns a coroutine object, not a result

-   Drive it with `send(None)`

-   `StopIteration` means the coroutine finished

</section>
<section class="slide" markdown="1">

## Await

-   `await` pauses a coroutine and yields control

-   The awaited object must have `__await__`

-   `Event.__await__` yields itself and returns a value on resume

</section>
<section class="slide" markdown="1">

## The Scheduler

-   `Task.step` drives one coroutine

-   A ready queue holds tasks waiting to run

-   `Environment.run` runs each task until its next `await`

</section>
