TARGETS=\
  source_sink.pdf \
  source_sink.svg \
  split_join.pdf \
  split_join.svg \
  flow_first.out \
  flow_second.out \
  flow_third.out

include ../../examples.mk

split_join.pdf split_join.svg: split_join.dot

source_sink.pdf source_sink.svg: source_sink.dot

%.pdf: %.dot
	dot -Tpdf $< > $@

%.svg: %.dot
	dot -Tsvg $< > $@
