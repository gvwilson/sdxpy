TARGETS=\
  hash_all.out \
  hash_stream.out \
  hash_stream_dracula.out \
  test_backup_manual.out

include ../examples.mk

hash_all.out: hash_all.sh hash_all.py
	bash $< 2>&1 > $@
