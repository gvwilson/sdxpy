include lib/mccole/mccole.mk

COLUMNS=72

BIN_PY = $(wildcard bin/*.py)
LIB_PY = $(wildcard lib/mccole/extensions/*.py)
SRC_PY = $(wildcard src/*/*.py)

## check: check source code style
.PHONY: check
check:
	-@flake8 --ignore=E302,E305 ${SRC_PY}
	-@black --check --line-length ${COLUMNS} ${SRC_PY}
	-@flake8 ${BIN_PY} ${LIB_PY}
	-@isort --check ${BIN_PY} ${LIB_PY}
	-@black --check ${BIN_PY} ${LIB_PY}

## fix: fix source code
.PHONY: fix
fix:
	@isort ${BIN_PY} ${LIB_PY}
	@black ${BIN_PY} ${LIB_PY}

## ---: ---
