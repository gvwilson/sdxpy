TARGETS=\
  test_direct.out \
  test_re.out

include ../../examples.mk

test_direct.out: test_direct.py direct.py
	pytest $< 2>&1 | grep FAILED > $@

test_re.out: test_re.py re_alt.py re_any.py re_base.py re_end.py re_lit.py re_start.py
	pytest $< 2>&1 > $@
