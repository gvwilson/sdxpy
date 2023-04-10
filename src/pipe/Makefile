TARGETS=\
  split_join.svg \
  workflow_first.out

include ../../examples.mk

split_join.svg: split_join.dot
	dot -Tsvg $< > $@
