from z3 import Bool, Solver, sat

def report(title, result):
    print(f"{title}: {result}")
    if result == sat:
        model = solver.model()
        for term in model:
            print(term, model[term])

A = Bool("A")
B = Bool("B")
C = Bool("C")

# [solve]
solver = Solver()
solver.add(A == B)
solver.add(B == C)
solver.add(A != C)
report("A == B & B == C & B != C", solver.check())
# [/solve]
