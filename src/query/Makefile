TARGETS=\
  aggregate.out \
  choose_columns.out \
  delay_columns.out \
  get_metadata.out \
  insert.out \
  select_all.out \
  simpler_metadata.out \
  where.out

%.out: %.py example.db
	python $< example.db > $@

include ../../examples.mk

insert.out: insert.py
	@rm -f temp.db
	@sqlite3 temp.db < example.sql
	python $< temp.db > $@
	@sqlite3 temp.db 'select * from person' >> $@
	@rm temp.db

example.db: example.sql
	@rm -f $@
	sqlite3 $@ < $<
