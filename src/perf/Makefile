SRC=df_col.py df_row.py df_base.py util.py
TARGETS=\
  analysis.svg \
  make.out \
  profile.out \
  timing.csv

include ../../examples.mk

analysis.pdf analysis.svg: timing.csv analysis.py
	python analysis.py

profile.out: profile.sh timing.py ${SRC}
	bash profile.sh > profile.out

timing.csv: timing.sh timing.py ${SRC}
	bash timing.sh > $@
