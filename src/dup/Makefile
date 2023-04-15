TARGETS=\
  naive_hash.out \
  naive_dracula.pdf \
  naive_dracula.svg \
  naive_dracula_unique.pdf \
  naive_dracula_unique.svg \
  sha256_dracula.pdf \
  sha256_dracula.svg

include ../../examples.mk

naive_dracula.pdf naive_dracula.svg naive_dracula_unique.pdf naive_dracula_unique.svg: naive_dracula.py naive_hash.py dracula.txt
	python naive_dracula.py

sha256_dracula.pdf sha256_dracula.svg: sha256_dracula.py dracula.txt
	python sha256_dracula.py
