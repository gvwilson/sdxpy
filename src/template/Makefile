TARGETS=\
  conditional.out \
  loop.out \
  multiple_variables.out \
  single_constant.out \
  single_variable.out \
  static_text.out \

include ../../examples.mk

EXTRAS = template.py vars.json

template.py: expander.py
	@touch $@

expander.py: env.py visitor.py z_if.py z_loop.py z_num.py z_var.py
	@touch $@

conditional.out: ${EXTRAS} conditional.ht
loop.out: ${EXTRAS} loop.ht
multiple_variables.out: ${EXTRAS} multiple_variables.ht
single_constant.out: ${EXTRAS} single_constant.ht
single_variable.out: ${EXTRAS} single_variable.ht
static_text.out: ${EXTRAS} static_text.ht
