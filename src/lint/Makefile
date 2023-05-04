TARGETS=\
  doc_sample.out \
  dump_ast_double.out \
  dump_ast_simple.out \
  find_duplicate_keys.out \
  find_unused_variables.out \
  has_duplicate_keys.out \
  inheritance_example.out \
  inject_exec.out \
  inject_make.out \
  inject_modified.out \
  inject_parse.out \
  unparse_exec.out \
  unparse_modified.out \
  walk_ast.out

include ../../examples.mk

doc_sample.out: doc_sample.py doc_extract.py doc_format.py
	python doc_format.py doc_sample.py > $@

dump_ast_double.out: dump_ast.py double.py
dump_ast_simple.out: dump_ast.py simple.py
find_unused_variables.out: has_unused_variables.py
find_duplicate_keys.out: has_duplicate_keys.py
inheritance_example.out: inheritance.py
inject_exec.out: inject.py add_double.py
inject_make.out: inject.py call.py
inject_modified.out: inject.py add_double.py
inject_parse.out: inject.py call.py
unparse_exec.out: unparse.py double_and_print.py
unparse_modified.out: unparse.py double_and_print.py
walk_ast.out: double.py
