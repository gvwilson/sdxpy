# ----------------------------------------------------------------------
# Generic McCole Makefile.
# ----------------------------------------------------------------------

# By default, show available commands (by finding '##' comments).
.DEFAULT: commands

# Where to find things relative to project root.
MCCOLE=./lib/mccole
MCCOLE_BIN=${MCCOLE}/bin

# Get local configuration from the Ivy configuration file.
CONFIG := ./config.py
ABBREV := $(shell python ${CONFIG} --abbrev)
BUILD_DATE := $(shell date '+%Y-%m-%d')
CHAPTERS := $(shell python ${CONFIG} --chapters)

# Direct variables.
BIN_PY := $(wildcard ${MCCOLE_BIN}/*.py)
LIB_PY := $(wildcard ${MCCOLE}/extensions/*.py)
EXAMPLES := $(patsubst %/Makefile,%,$(wildcard src/*/Makefile))
HTML := info/head.html info/foot.html
INFO := info/bibliography.bib info/credits.yml info/glossary.yml info/links.yml
IVY :=  $(wildcard ${MCCOLE}/extensions/*.*) $(wildcard ${MCCOLE}/resources/*.*) $(wildcard ${MCCOLE}/templates/*.*)
TEX := info/head.tex info/foot.tex
TEX_COPY := info/krantz.cls info/dedication.tex
PAGES := $(wildcard src/*.md) $(wildcard src/*/index.md)
SLIDES := $(wildcard src/*/slides.html)
SRC_SVG := $(wildcard src/*/*.svg)

# Calculated variables.
DOCS := $(patsubst src/%.md,docs/%.html,$(PAGES)) $(patsubst src/%/slides.html,docs/%/slides/index.html,$(SLIDES))
FIG_PDF := $(patsubst src/%.svg,docs/%.pdf,${FIG_SVG})
SRC_PDF := $(patsubst src/%.svg,src/%.pdf,${SRC_SVG})
DOCS_PDF := $(patsubst src/%.pdf,docs/%.pdf,${SRC_PDF})
STEM := ${ABBREV}-${BUILD_DATE}
SRC := ${PAGES} ${SLIDES}

# Keep the PDF versions of diagrams under the 'src' directory.
.PRECIOUS: ${SRC_PDF}

# Where to run the local preview server.
PORT := 4000

## ---: ---

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## build: rebuild site without running server
build: ./docs/index.html
./docs/index.html: ${SRC} ${SRC_SVG} ${INFO} ${IVY} config.py
	ivy build && touch $@

## serve: build site and run server
.PHONY: serve
serve:
	ivy watch --port ${PORT}

## pdf: create PDF version of material
pdf: docs/${STEM}.tex ${DOCS_PDF}
	cp info/bibliography.bib docs
	cd docs && pdflatex ${STEM}
	cd docs && biber ${STEM}
	cd docs && makeindex ${STEM}
	cd docs && pdflatex ${STEM}
	cd docs && pdflatex ${STEM}

## ---: ---

## lint: check project structure
.PHONY: lint
lint: clean build
	@python ${MCCOLE_BIN}/lint.py \
	--config config.py \
	--dom ${MCCOLE}/dom.yml

## inclusions: compare inclusions in prose and slides
.PHONY: inclusions
inclusions:
	@python ${MCCOLE_BIN}/inclusions.py --pages ${CHAPTERS}

## examples: re-run examples
.PHONY: examples
examples:
	@for d in ${EXAMPLES}; do echo ""; echo $$d; make -C $$d; done

## fonts: check fonts in diagrams
.PHONY: fonts
fonts:
	@python ${MCCOLE_BIN}/check_svg_fonts.py $(SRC_SVG)

## spelling: check spelling against known words
.PHONY: spelling
spelling:
	@make wordlist \
	| python ${MCCOLE_BIN}/post_spellcheck.py info/wordlist.txt

## wordlist: make a list of unknown and unused words
.PHONY: wordlist
wordlist: ./docs/index.html
	@python ${MCCOLE_BIN}/pre_spellcheck.py --pages ${PAGES} --slides ${SLIDES} \
	| aspell -H list \
	| sort \
	| uniq

## ---: ---

## html: create single-page HTML
html: docs/all.html
docs/all.html: ./docs/index.html ${HTML} ${MCCOLE_BIN}/single.py
	python ${MCCOLE_BIN}/single.py \
	--head info/head.html \
	--foot info/foot.html \
	--root docs \
	--title "$$(python ${CONFIG} --title)" \
	--tagline "$$(python ${CONFIG} --tagline)" \
	> docs/all.html

## latex: create LaTeX document
latex: docs/${STEM}.tex
docs/${STEM}.tex: docs/all.html ${MCCOLE_BIN}/html2tex.py ${CONFIG} ${TEX} ${TEX_COPY}
	python ${MCCOLE_BIN}/html2tex.py \
	--head info/head.tex \
	--foot info/foot.tex \
	< docs/all.html \
	> docs/${STEM}.tex
	python ${CONFIG} --latex > docs/config.tex
	cp ${TEX_COPY} docs

## pdf-once: create PDF document with a single compilation
pdf-once: docs/${STEM}.tex ${DOCS_PDF}
	cd docs && pdflatex ${STEM}

## diagrams: convert diagrams from SVG to PDF
diagrams: ${DOCS_PDF}
src/%.pdf: src/%.svg
	${MCCOLE_BIN}/convert_drawio.sh $< $@
docs/%.pdf: src/%.pdf
	cp $< $@

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

## publisher: create archive to send to publisher
.PHONY: publisher
publisher:
	zip -r ${STEM}.zip \
	docs/${STEM}.tex \
	docs/bibliography.bib \
	docs/config.tex \
	docs/dedication.tex \
	docs/krantz.cls \
	docs/*/*.pdf

## web: export files for publishing on the web
.PHONY: web
web:
	@if [ -z ${MCCOLE} ]; then echo "Must set MCCOLE" 1>&2; exit 1; fi
	rm -rf ${MCCOLE}
	MCCOLE=${MCCOLE} ivy build
	@zip -q -r ${MCCOLE}/${ABBREV}-examples.zip docs \
	-i '*.ht' '*.json' '*.out' '*.py' '*.sh' '*.txt' '*.yml' \
	-x '*.html'

## ---: ---

## check: check source code
.PHONY: check
check:
	-@flake8 ${BIN_PY} ${LIB_PY}
	-@isort --check ${BIN_PY} ${LIB_PY}
	-@black --check ${BIN_PY} ${LIB_PY}

## fix: fix source code
.PHONY: fix
fix:
	@isort ${BIN_PY} ${LIB_PY}
	@black ${BIN_PY} ${LIB_PY}

## profile: profile compilation
.PHONY: profile
profile:
	python ${MCCOLE_BIN}/run_profile.py

## clean: clean up stray files
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -name '*.bkp' -exec rm {} \;
	@find . -name '.*.dtmp' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r
	@rm -f \
	docs/*.aux \
	docs/*.bbl \
	docs/*.bcf \
	docs/*.blg \
	docs/*.idx \
	docs/*.ilg \
	docs/*.ind \
	docs/*.log \
	docs/*.out \
	docs/*.pdf \
	docs/*.run.xml \
	docs/*.tex \
	docs/*.toc

## ---: ---

## status: status of chapters
.PHONY: status
status:
	@python ${MCCOLE_BIN}/status.py --config config.py --readme README.md
	@python ${MCCOLE_BIN}/check_prose_slides.py --config config.py

## count: words per file
.PHONY: count
count:
	@(wc -w ${PAGES} && grep -c '\[% figure' ${PAGES}) | python ${MCCOLE_BIN}/count.py

## valid: run html5validator on generated files
.PHONY: valid
valid: docs/all.html
	@html5validator --root docs ${DOCS} \
	--ignore \
	'Attribute "ix-key" not allowed on element "span"' \
	'Attribute "ix-ref" not allowed on element "a"' \
	'Attribute "markdown" not allowed on element'

## vars: show variables
.PHONY: vars
vars:
	@echo ABBREV ${ABBREV}
	@echo BUILD_DATE ${BUILD_DATE}
	@echo DOCS ${DOCS}
	@echo DOCS_PDF ${DOCS_PDF}
	@echo EXPORT_FILES ${EXPORT_FILES}
	@echo HTML ${HTML}
	@echo INFO ${INFO}
	@echo IVY ${IVY}
	@echo SRC ${SRC}
	@echo SRC_PDF ${SRC_PDF}
	@echo SRC_SVG ${SRC_SVG}
	@echo STEM ${STEM}
	@echo TEX ${TEX}
