include lib/mccole/mccole.mk

COLUMNS=72

SRC_PY = $(wildcard src/*/*.py)

## release: make a release
.PHONY: release
ifeq ($(origin SDXPY_RELEASE),undefined)
release:
	@echo "SDXPY_RELEASE not defined"
else
release:
	rm -rf docs ${SDXPY_RELEASE}
	make build
	cp -r docs ${SDXPY_RELEASE}
	find ${SDXPY_RELEASE} \( -name .DS_Store -or -name '*.pdf' -or -name '*.aux' -or -name '*.bbl' -or -name '*.bcf' -or -name '*.bib' -or -name '*.blg' -or -name '*.cls' -or -name '*.idx' -or -name '*.ilg' -or -name '*.ind' -or -name '*.log' -or -name '*.tex' -or -name '*.toc' \) -exec rm {} +
	cd ${SDXPY_RELEASE} && zip -q -r ${ABBREV}-examples.zip . -i '*.as' '*.ht' '*.json' '*.mx' '*.out' '*.py' '*.sh' '*.tll' '*.txt' '*.yml'
endif

## style: check source code style
.PHONY: style
style:
	-@flake8 --ignore=E302,E305 ${SRC_PY}
	-@black --check --line-length ${COLUMNS} ${SRC_PY}
