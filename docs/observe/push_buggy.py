from push_simple import Node

a = Node("A")
b = Node("B")
a.watch(b)
b.watch(a)
a.notify()
