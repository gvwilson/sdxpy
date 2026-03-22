from delay_queue import Node, Queue, Source

queue = Queue()
a = Node(queue, "A")
b = Node(queue, "B")
c = Node(queue, "C")
d = Source(queue, "D")
a.watch(b)
a.watch(c)
b.watch(d)
c.watch(d)
d.notify()
queue.run(verbose=True)
