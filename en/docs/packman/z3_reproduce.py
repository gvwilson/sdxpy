from z3 import Bool, And, Or, Not, Implies, Solver

A1 = Bool("A1")
A2 = Bool("A2")
A3 = Bool("A3")

B1 = Bool("B1")
B2 = Bool("B2")
B3 = Bool("B3")

C1 = Bool("C1")
C2 = Bool("C2")

solver = Solver()

solver.add(Or(A1, A2, A3))

solver.add(Implies(A3, Not(Or(A1, A2))))
solver.add(Implies(A2, Not(Or(A1, A3))))
solver.add(Implies(A1, Not(Or(A1, A2))))

solver.add(Implies(B3, Not(Or(B1, B2))))
solver.add(Implies(B2, Not(Or(B1, B3))))
solver.add(Implies(B1, Not(Or(B1, B2))))

solver.add(Implies(C1, Not(C2)))
solver.add(Implies(C2, Not(C1)))

solver.add(Implies(A3, And(Or(B3, B2), C2)))
solver.add(Implies(A2, And(B2, Or(C2, C1))))
solver.add(Implies(A1, B1))

solver.add(Implies(B3, C2))
solver.add(Implies(B2, C1))
solver.add(Implies(B1, C1))

print("result", solver.check(), solver.model())
