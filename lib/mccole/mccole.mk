# ----------------------------------------------------------------------
# Generic McCole Makefile.
# ----------------------------------------------------------------------

# By default, show available commands (by finding '##' comments).
.DEFAULT: commands

# Get local configuration from the Ivy configuration file.
CONFIG := ./config.py
ABBREV := $(shell python ${CONFIG} --abbrev)
BUILD_DATE := $(shell date '+%Y-%m-%d')
CHAPTERS := $(patsubst %,src/%/index.md,$(shell python ${CONFIG} --chapters))

# Direct variables.
EXAMPLES := $(patsubst %/Makefile,%,$(wildcard src/*/Makefile))
HTML := info/head.html info/foot.html
INFO := info/bibliography.bib info/credits.yml info/glossary.yml info/links.yml
IVY := $(wildcard lib/mccole/*/*.*)
TEX := info/head.tex info/foot.tex
TEX_COPY := info/krantz.cls info/dedication.tex
MARKDOWN := $(wildcard src/*.md) $(wildcard src/*/index.md)
SLIDES := $(wildcard src/*/slides/index.html)
SRC_SVG := $(wildcard src/*/*.svg)

# Calculated variables.
DOCS := docs/index.html $(patsubst src/%.md,docs/%.html,$(wildcard src/*/index.md)) $(patsubst src/%/slides/index.html,docs/%/slides/index.html,$(SLIDES))
FIG_PDF := $(patsubst src/%.svg,docs/%.pdf,${FIG_SVG})
SRC_PDF := $(patsubst src/%.svg,src/%.pdf,${SRC_SVG})
DOCS_PDF := $(patsubst src/%.pdf,docs/%.pdf,${SRC_PDF})
STEM := ${ABBREV}-${BUILD_DATE}
SRC := ${MARKDOWN} ${SLIDES}

# Keep the PDF versions of diagrams under the 'src' directory.
.PRECIOUS: ${SRC_PDF}

# Where to run the local preview server.
PORT := 4000

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## build: rebuild site without running server
build: ./docs/index.html
./docs/index.html: ${SRC} ${INFO} ${IVY} config.py
	ivy build && touch $@

## serve: build site and run server
.PHONY: serve
serve:
	ivy watch --port ${PORT}

## html: create single-page HTML
html: docs/all.html
docs/all.html: ./docs/index.html ${HTML} bin/single.py
	python ./bin/single.py \
	--head info/head.html \
	--foot info/foot.html \
	--root docs \
	--title "$$(python ${CONFIG} --title)" \
	--tagline "$$(python ${CONFIG} --tagline)" \
	> docs/all.html

## latex: create LaTeX document
latex: docs/${STEM}.tex
docs/${STEM}.tex: docs/all.html bin/html2tex.py ${CONFIG} ${TEX} ${TEX_COPY}
	python ./bin/html2tex.py \
	--head info/head.tex \
	--foot info/foot.tex \
	< docs/all.html \
	> docs/${STEM}.tex
	python ${CONFIG} --latex > docs/config.tex
	cp ${TEX_COPY} docs

## pdf: create PDF version of material
pdf: docs/${STEM}.tex ${DOCS_PDF}
	cp info/bibliography.bib docs
	cd docs && pdflatex ${STEM}
	cd docs && biber ${STEM}
	cd docs && makeindex ${STEM}
	cd docs && pdflatex ${STEM}
	cd docs && pdflatex ${STEM}

## pdf-once: create PDF document with a single compilation
pdf-once: docs/${STEM}.tex ${DOCS_PDF}
	cd docs && pdflatex ${STEM}

## diagrams: convert diagrams from SVG to PDF
diagrams: ${DOCS_PDF}
src/%.pdf: src/%.svg
	./bin/convert_drawio.sh $< $@
docs/%.pdf: src/%.pdf
	cp $< $@

## clean: clean up stray files
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -name '*.bkp' -exec rm {} \;
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

## lint: check project structure
.PHONY: lint
lint: clean build
	@python ./bin/lint.py \
	--config config.py \
	--dom ./lib/mccole/dom.yml

## examples: re-run examples
.PHONY: examples
examples:
	@for d in ${EXAMPLES}; do echo ""; echo $$d; make -C $$d; done

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

## count: words per file
.PHONY: count
count:
	@(wc -w ${MARKDOWN} && grep -c '\[% figure' ${MARKDOWN}) | python bin/count.py

## exercises: exercises per file
.PHONY: exercises
exercises:
	@fgrep -c '{: .exercise}' $(CHAPTERS) | sed 's/\(.*\):\(.*\)/\2 \1/g'

## valid: run html5validator on generated files
.PHONY: valid
valid: docs/all.html
	@html5validator --root docs ${DOCS} \
	--ignore \
	'Attribute "ix-key" not allowed on element "span"' \
	'Attribute "ix-ref" not allowed on element "a"' \
	'Attribute "markdown" not allowed on element'

## profile: profile compilation
.PHONY: profile
profile:
	python bin/run_profile.py

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
