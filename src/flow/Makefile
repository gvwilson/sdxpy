TARGETS=\
  source_sink.svg \
  split_join.svg \
  flow_first.out \
  flow_second.out \
  flow_third.out

include ../../examples.mk

split_join.svg: split_join.dot
	dot -Tsvg $< > $@

source_sink.svg: source_sink.dot
	dot -Tsvg $< > $@
