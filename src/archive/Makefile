TARGETS=\
  hash_all.out \
  hash_stream.out \
  hash_stream_dracula.out \
  naive_dracula.csv \
  test_naive_hash.out \
  test_backup_manual.out

include ../../examples.mk

hash_all.out: hash_all.sh hash_all.py
	bash $< 2>&1 > $@

naive_dracula.csv: naive_dracula.py naive_hash.py
	python $< > $@

test_naive_hash.py: naive_hash.py
