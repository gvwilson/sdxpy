include lib/mccole/mccole.mk

BIN_PY = $(wildcard bin/*.py)
SRC_PY = $(wildcard src/*/*.py)

## check: check source code style
.PHONY: check
check:
	-@flake8 --ignore=E302,E305 ${SRC_PY}
	-@flake8 ${BIN_PY}
	-@isort --check ${BIN_PY}
	-@black --check ${BIN_PY}

## fix: fix source code
.PHONY: fix
fix:
	@isort ${BIN_PY}
	@black ${BIN_PY}

## ---: ---
