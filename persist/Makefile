TARGETS=\
  attr.out \
  save_aliasing.out \
  save_builtin.out \
  test_aliasing.out \
  test_aliasing_wrong.out \
  test_builtin.out

include ../../examples.mk

test_aliasing.out: test_aliasing.py aliasing.py
	COLUMNS=${COLUMNS} pytest $< | ${REFORMAT} > $@

test_aliasing_wrong.out: test_aliasing_wrong.py aliasing_wrong.py
	COLUMNS=${COLUMNS} pytest $< | ${REFORMAT} > $@

test_builtin.out: test_builtin.py builtin.py
	COLUMNS=${COLUMNS} pytest $< | ${REFORMAT} > $@
