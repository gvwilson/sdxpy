from z3 import Int, And, Or, Solver

a = Int("a")
b = Int("b")
c = Int("c")
lengths = (a > 0, b > 0, c > 0)

equilateral = And(a == b, b == c, c == a)
solver = Solver()
solver.add(lengths)
solver.add(equilateral)
print("equilateral", solver.check(), solver.model())

scalene = And(a != b, b != c, c != a)
solver = Solver()
solver.add(lengths)
solver.add(scalene)
print("scalene", solver.check(), solver.model())

isosceles = Or(
    And(a == b, c != a),
    And(a == b, b != c),
    And(a != b, b == c)
)
solver = Solver()
solver.add(lengths)
solver.add(isosceles)
print("isosceles", solver.check(), solver.model())
