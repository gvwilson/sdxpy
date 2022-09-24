TARGETS=\
  count_up.out \
  fill_array.out \
  halt.out \
  print_r1.out

include ../examples.mk

%.out: %_run.sh %.mx vm.py
	bash $< 2>&1 > $@

%.mx: %_assemble.sh %.as assembler.py
	bash $< 2>&1 > $@

vm.py: vm_base.py
	@touch $@

data_allocator.py: assembler.py
	@touch $@
