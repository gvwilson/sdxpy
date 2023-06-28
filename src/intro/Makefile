TARGETS=\
  syllabus.pdf \
  syllabus.png \
  syllabus.svg

include ../../examples.mk

syllabus.pdf: syllabus.dot
	dot -Tpdf $< > $@

syllabus.png: syllabus.dot
	dot -Tpng $< > $@

syllabus.svg: syllabus.dot
	dot -Tsvg $< > $@
