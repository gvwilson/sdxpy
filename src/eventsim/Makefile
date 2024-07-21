TARGETS=\
  multiprocess.out \
  pc_stats.out \
  pc_stats_multi.out \
  wait_and_work.out \
  wait_event.out \
  wait_work_record.out

include ../../examples.mk

pc_stats.out: pc_stats.py
	python $< 4219384 1000 10 > $@

pc_stats_multi.out: pc_stats_multi.py
	python $< 4219384 1000 10 3 > $@
