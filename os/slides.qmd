---
title: "A Micro-Operating System"
---

<section class="slide" markdown="1">

## Overview

-   An OS runs many processes and lets them block on I/O

-   We turn the event loop into a tiny OS

-   No virtual memory, no protection — just processes and devices

</section>
<section class="slide" markdown="1">

## The Kernel and Its Clock

-   A ready queue runs work immediately

-   A heap schedules work for the future

-   `sleep` returns a `Timeout` that fires later

</section>
<section class="slide" markdown="1">

## Processes

-   A process is a named coroutine

-   `await` blocks the process

-   The kernel re-queues it when its event fires

</section>
<section class="slide" markdown="1">

## Devices

-   A device is a queue

-   `await device.get()` blocks until data arrives

-   `put` wakes a waiting process or buffers the value

</section>
