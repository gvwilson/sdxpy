TARGETS=\
  profile.out \
  timing.csv

include ../../examples.mk

timing.csv: timing.sh timing.py
	bash $< 2>&1 > $@
