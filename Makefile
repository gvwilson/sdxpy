include lib/mccole/mccole.mk

COLUMNS=72

SRC_PY = $(wildcard src/*/*.py)

## style: check source code style
.PHONY: style
style:
	-@flake8 --ignore=E302,E305 ${SRC_PY}
	-@black --check --line-length ${COLUMNS} ${SRC_PY}
