TARGETS=\
  fail_large.out \
  log_keystrokes.out

include ../examples.mk

fail_large.out: fail_large.py
	python $< | cut -d '>' -f 3 > $@

log_keystrokes.out: log_keystrokes.sh log_keystrokes.py
	bash $<
