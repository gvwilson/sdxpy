TARGETS=\
  callable.out \
  decorator_param.out \
  decorator_simple.out \
  mock_object.out \
  wrap_capture.out \
  wrap_infinite.out \
  wrap_param.out

include ../../examples.mk

wrap_infinite.out: wrap_infinite.sh wrap_infinite.py
	bash $< > $@ 2> /dev/null
