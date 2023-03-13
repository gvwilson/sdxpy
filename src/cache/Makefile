TARGETS=\
  test_cache_filesystem.out \
  test_cache_limited.out \
  test_index_csv.out \
  test_io.out

include ../../examples.mk

test_cache_filesystem.out: test_cache_filesystem.py cache_filesystem.py index_csv.py
	pytest $< 2>&1 > $@
test_cache_limited.out: test_cache_limited.py cache_limited.py index_csv.py
	pytest $< 2>&1 > $@
test_index_csv.out: test_index_csv.py index_base.py index_csv.py
	pytest $< 2>&1 > $@
test_io.out: test_io.py cache_limited.py index_csv.py cache_io.py
	pytest $< 2>&1 > $@
