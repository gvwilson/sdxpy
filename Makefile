.DEFAULT: commands

# Local configuration.
ABBREV := $(shell python ./config.py --abbrev)

# Direct variables.
HTML := info/head.html info/foot.html
INFO := info/bibliography.bib info/credits.yml info/glossary.yml info/links.yml
FIG_SVG := $(wildcard src/*/*.svg)
IVY := $(wildcard lib/mccole/*/*.*)
TEX := info/head.tex info/foot.tex
SRC := $(wildcard *.md) $(wildcard src/*.md) $(wildcard src/*/index.md)

# Calculated variables.
DOCS := docs/index.html $(patsubst src/%.md,docs/%.html,$(wildcard src/*/index.md))
FIG_PDF := $(patsubst src/%.svg,docs/%.pdf,${FIG_SVG})

PORT := 4000

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild site without running server
build: ./docs/index.html
./docs/index.html: ${SRC} ${INFO} ${IVY} config.py
	ivy build && touch $@

## serve: build site and run server
.PHONY: serve
serve:
	ivy watch --port ${PORT}

## single: create single-page HTML
single: docs/all.html
docs/all.html: ./docs/index.html ${HTML} bin/single.py
	python ./bin/single.py \
	--head info/head.html \
	--foot info/foot.html \
	--root docs \
	--title "$$(python ./config.py --title)" \
	--tagline "$$(python ./config.py --tagline)" \
	> docs/all.html

## latex: create LaTeX document
latex: docs/${ABBREV}.tex
docs/${ABBREV}.tex: docs/all.html ${TEX} bin/html2tex.py ./config.py
	python ./bin/html2tex.py --head info/head.tex --foot info/foot.tex < docs/all.html > docs/${ABBREV}.tex
	python ./config.py --latex > docs/config.tex

## pdf: create PDF document
pdf: docs/${ABBREV}.tex ${FIG_PDF}
	cp info/bibliography.bib docs
	cd docs && pdflatex ${ABBREV}
	cd docs && biber ${ABBREV}
	cd docs && makeindex ${ABBREV}
	cd docs && pdflatex ${ABBREV}
	cd docs && pdflatex ${ABBREV}

docs/%.pdf: src/%.svg
	@convert $< $@

## clean: clean up stray files
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r

## check: check code and project structure
.PHONY: check
check: lint
	-flake8
	-isort --check .
	-black --check .

## lint: check project structure
.PHONY: lint
lint:
	python ./bin/lint.py --dom info/dom.yml --links info/links.yml --html docs --src src

## spelling: check spelling against known words
.PHONY: spelling
spelling:
	@make wordlist \
	| python ./bin/post_spellcheck.py info/wordlist.txt

## wordlist: make a list of unknown and unused words
.PHONY: wordlist
wordlist: ./docs/index.html
	@cat ${DOCS} \
	| python ./bin/pre_spellcheck.py \
	| aspell -H list \
	| sort \
	| uniq

## valid: run html5validator on generated files
.PHONY: valid
valid: docs/all.html
	@html5validator --root docs ${DOCS} \
	--ignore \
	'Attribute "ix-key" not allowed on element "span"' \
	'Attribute "ix-ref" not allowed on element "a"' \
	'Attribute "markdown" not allowed on element'

## release: create archive of standard files
.PHONY: release
release:
	zip -r mccole.zip \
	CODE_OF_CONDUCT.md \
	CONTRIBUTING.md \
	LICENSE.md \
	Makefile \
	bin \
	info/dom.yml \
	info/*.html \
	info/*.tex \
	lib \
	src/bibliography \
	src/conduct \
	src/contents \
	src/credits \
	src/glossary \
	src/license \
	src/links \
	src/syllabus \
	-x "*__pycache__*"

## vars: show variables
.PHONY: vars
vars:
	@echo ABBREV ${ABBREV}
	@echo DOCS ${DOCS}
	@echo FIG_SVG ${FIG_SVG}
	@echo FIG_PDF ${FIG_PDF}
	@echo HTML ${HTML}
	@echo INFO ${INFO}
	@echo IVY ${IVY}
	@echo SRC ${SRC}
	@echo TEX ${TEX}
