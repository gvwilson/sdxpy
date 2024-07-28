TARGETS=\
  binary_perf.out \
  compress_perf.out \
  frequency.pdf \
  frequency.svg
TEXT = ../intro/index.md

include ../../examples.mk

binary_perf.out: binary.py
	@echo "binary performance"
	@rm -f $@
	@echo "original" >> $@ && cat ${TEXT} | wc -c >> $@
	@echo "compressed" >> $@ && python $< c < ${TEXT} | wc -c >> $@

compress_perf.out: compress.py
	@echo "compress performance"
	@rm -f $@
	@echo "original" >> $@ && cat ${TEXT} | wc -c >> $@
	@echo "compressed" >> $@ && python $< c < ${TEXT} | wc -c >> $@

frequency.pdf frequency.svg: frequency.py
	python $< frequency < ${TEXT}
