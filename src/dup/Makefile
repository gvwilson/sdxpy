TARGETS=\
  brute_force_1.out \
  dup.out \
  grouped.out \
  naive_hash.out \
  naive_dracula.pdf \
  naive_dracula.svg \
  naive_dracula_unique.pdf \
  naive_dracula_unique.svg \
  sha256_dracula.pdf \
  sha256_dracula.svg \
  using_sha256.out

include ../../examples.mk

naive_dracula.pdf naive_dracula.svg naive_dracula_unique.pdf naive_dracula_unique.svg: naive_dracula.py naive_hash.py dracula.txt
	python naive_dracula.py

sha256_dracula.pdf sha256_dracula.svg: sha256_dracula.py dracula.txt
	python sha256_dracula.py
