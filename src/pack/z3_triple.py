from z3 import Bool, And, Or, Not, Implies, Solver

# [setup]
A1 = Bool("A.1")
A2 = Bool("A.2")
A3 = Bool("A.3")

B1 = Bool("B.1")
B2 = Bool("B.2")
B3 = Bool("B.3")

C1 = Bool("C.1")
C2 = Bool("C.2")
# [/setup]

# [top]
solver = Solver()
solver.add(Or(A1, A2, A3))
# [/top]

# [exclusive]
solver.add(Implies(A1, Not(Or(A2, A3))))
solver.add(Implies(A2, Not(Or(A1, A3))))
solver.add(Implies(A3, Not(Or(A1, A2))))
# [/exclusive]

solver.add(Implies(B1, Not(Or(B2, B3))))
solver.add(Implies(B2, Not(Or(B1, B3))))
solver.add(Implies(B3, Not(Or(B1, B2))))

solver.add(Implies(C1, Not(C2)))
solver.add(Implies(C2, Not(C1)))

# [depends]
solver.add(Implies(A3, And(Or(B3, B2), C2)))
solver.add(Implies(A2, And(B2, Or(C2, C1))))
solver.add(Implies(A1, B1))
solver.add(Implies(B3, C2))
solver.add(Implies(B2, C1))
solver.add(Implies(B1, C1))

print("result", solver.check(), solver.model())
# [/depends]
