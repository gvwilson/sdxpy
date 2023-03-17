TARGETS=\
  syllabus.pdf \
  syllabus.svg

include ../../examples.mk

syllabus.pdf: syllabus.dot
	dot -Tpdf $< > $@

syllabus.svg: syllabus.dot
	dot -Tsvg $< > $@
