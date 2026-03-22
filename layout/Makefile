TARGETS=\
  test_easy_mode.out \
  test_placed.out \
  test_wrapped.out

include ../../examples.mk

test_easy_mode.out: test_easy_mode.py easy_mode.py
	COLUMNS=${COLUMNS} pytest $< > $@

test_placed.out: test_placed.py placed.py
	COLUMNS=${COLUMNS} pytest $< > $@

test_wrapped.out: test_wrapped.py wrapped.py
	COLUMNS=${COLUMNS} pytest $< > $@
