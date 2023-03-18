TARGETS=\
  test_glob_problem.out

include ../../examples.mk

test_glob_problem.out: test_glob_problem.py glob_lit.py glob_either.py
	-COLUMNS=${COLUMNS} pytest --tb=no $< > $@
