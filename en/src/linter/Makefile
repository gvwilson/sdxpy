TARGETS=\
  doc_sample.out \
  dump_ast_double.out \
  dump_ast_simple.out \
  find_unused_variables.out \
  has_duplicate_keys_ast.out \
  inheritance_example.out \
  walk_ast.out

include ../../examples.mk

doc_sample.out: doc_sample.py doc_extract.py doc_format.py
	python doc_format.py doc_sample.py > $@

dump_ast_simple.out: dump_ast.py simple.py
dump_ast_double.out: dump_ast.py double.py
find_unused_variables.out: has_unused_variables.py
has_duplicate_keys_ast.out: has_duplicate_keys.py dump_ast.py
inheritance_example.out: inheritance.py
walk_ast.out: double.py
