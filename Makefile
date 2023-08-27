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
	rm -rf docs
	make build
	rm -rf ${SDXPY_RELEASE}
	mkdir ${SDXPY_RELEASE}
	(cd docs && tar cf - $$(find . -name '*.css' -o -name '*.html' -o -name '*.ico' -o -name '*.jpg' -o -name '*.js' -o -name '*.png' -o -name '*.svg' -o -name '*.webp')) \
	| (cd ${SDXPY_RELEASE} && tar xf -)
	cd docs && zip -q -r ${SDXPY_RELEASE}/${ABBREV}-examples.zip . \
	-i '*.ht' '*.json' '*.out' '*.py' '*.sh' '*.tll' '*.txt' '*.yml' \
	-x '*.css' '*.html' '*.ico' '*.js' '*.svg' '*.webp'
	cd ${SDXPY_RELEASE} && unzip -q ${ABBREV}-examples.zip
endif

## style: check source code style
.PHONY: style
style:
	-@flake8 --ignore=E302,E305 ${SRC_PY}
	-@black --check --line-length ${COLUMNS} ${SRC_PY}
