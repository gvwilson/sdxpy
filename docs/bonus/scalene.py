from z3 import Int, And, Solver

A = Int("A")
B = Int("B")
C = Int("C")
lengths = (A > 0, B > 0, C > 0)

# [scalene]
scalene = And(A != B, B != C, C != A)
solver = Solver()
solver.add(lengths)
solver.add(scalene)
print("scalene", solver.check(), solver.model())
# [/scalene]
