TARGETS=\
  adder.out \
  closure.out \
  dynamic.out \
  func.out \
  oop.out \
  decorator_param.out \
  decorator_simple.out \
  wrap_capture.out \
  wrap_infinite.out \
  wrap_param.out

include ../../examples.mk

dynamic.out: dynamic.tll
func.out: func.tll

wrap_infinite.out: wrap_infinite.sh wrap_infinite.py
	bash $< > $@ 2> /dev/null
