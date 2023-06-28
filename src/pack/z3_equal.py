from z3 import sat, unsat

# [setup]
from z3 import Bool, Solver

A = Bool("A")
B = Bool("B")
C = Bool("C")
# [/setup]

# [report]
def report(title, result):
    print(f"{title}: {result}")
    if result == sat:
        model = solver.model()
        for term in model:
            print(term, model[term])
# [/report]

# [solve]
solver = Solver()
solver.add(A == B)
solver.add(B == C)
report("A == B & B == C", solver.check())
# [/solve]
