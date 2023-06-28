TARGETS=\
  dump_ast_double.out \
  dump_ast_simple.out \
  find_duplicate_keys.out \
  find_unused_variables.out \
  has_duplicate_keys.out \
  walk_ast.out

include ../../examples.mk

doc_sample.out: doc_sample.py doc_extract.py doc_format.py
	python doc_format.py doc_sample.py > $@

dump_ast_double.out: dump_ast.py double.py
dump_ast_simple.out: dump_ast.py simple.py
find_unused_variables.out: has_unused_variables.py
find_duplicate_keys.out: has_duplicate_keys.py
walk_ast.out: double.py
