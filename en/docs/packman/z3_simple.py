from z3 import Bool, And, Or, Not, Implies, Solver, sat, unsat

A = Bool("A")
B = Bool("B")
C1 = Bool("C1")
C2 = Bool("C2")

solver = Solver()

solver.add(A)
solver.add(Implies(A, B))
solver.add(Implies(A, C1))
solver.add(Implies(B, C2))
solver.add(Implies(C1, Not(C2)))
solver.add(Implies(C2, Not(C1)))

result = solver.check()
print("result", result)
if result == sat:
    model = solver.model()
    for term in model:
        print(term, model[term])
