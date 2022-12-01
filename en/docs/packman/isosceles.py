from z3 import Int, And, Or, Solver

A = Int("A")
B = Int("B")
C = Int("C")
lengths = (A > 0, B > 0, C > 0)

# [isosceles]
isosceles = Or(
    And(A == B, C != A),
    And(A == B, B != C),
    And(A != B, B == C)
)
solver = Solver()
solver.add(lengths)
solver.add(isosceles)
print("isosceles", solver.check(), solver.model())
# [/isosceles]
