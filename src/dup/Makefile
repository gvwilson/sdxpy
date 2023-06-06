TARGETS=\
  brute_force_1.out \
  dup.out \
  grouped.out \
  naive_hash.out \
  naive_dracula.pdf \
  naive_dracula.svg \
  naive_dracula_unique.pdf \
  naive_dracula_unique.svg \
  using_sha256.out

include ../../examples.mk

naive_dracula.pdf naive_dracula.svg naive_dracula_unique.pdf naive_dracula_unique.svg: naive_dracula.py naive_hash.py dracula.txt
	python naive_dracula.py
