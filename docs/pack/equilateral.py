from z3 import Int, And, Or, Solver

# [setup]
A = Int("A")
B = Int("B")
C = Int("C")
lengths = (A > 0, B > 0, C > 0)
# [/setup]

# [equilateral]
equilateral = And(A == B, B == C, C == A)
solver = Solver()
solver.add(lengths)
solver.add(equilateral)
print("equilateral", solver.check(), solver.model())
# [/equilateral]
