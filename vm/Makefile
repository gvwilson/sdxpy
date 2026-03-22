TARGETS=\
  count_up.out \
  fill_array.out \
  halt.out \
  print_r1.out

.PRECIOUS: $(patsubst %.out,%.mx,${TARGETS})

include ../../examples.mk

%.out: %_run.sh %.mx vm.py
	bash $< 2>&1 > $@

%.mx: %_assemble.sh %.as
	bash $< 2>&1 > $@

%_assemble.sh: assembler.py
	@touch $@

fill_array_assemble.sh: arrays.py
	@touch $@

%_run.sh: vm.py
	@touch $@

arrays.py: assembler.py
	@touch $@

assembler.py: architecture.py
	@touch $@

vm.py: architecture.py
	@touch $@
