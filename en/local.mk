PYTHON_SRC = $(wildcard bin/*.py) $(wildcard src/*/*.py)

## ---: -------------------------------------

## check: check source code style
.PHONY: check
check:
	-flake8 ${PYTHON_SRC}
	-isort --check ${PYTHON_SRC}
	-black --check ${PYTHON_SRC}
