# ----------------------------------------------------------------------
# Generic McCole Makefile.
# ----------------------------------------------------------------------

# By default, show available commands (by finding '##' comments).
.DEFAULT: commands

# Get the absolute path to this file from wherever it is included.
# See https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
MCCOLE:=$(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

# Define the project root as the directory this file is included from.
ROOT:=.

# Get local configuration from the Ivy configuration file.
CONFIG := ${ROOT}/config.py
ABBREV := $(shell python ${CONFIG} --abbrev)
BUILD_DATE := $(shell date '+%Y-%m-%d')
CHAPTERS := $(shell python ${CONFIG} --chapters)
TITLE := $(shell python ${CONFIG} --title)

# Direct variables.
BIN_PY := $(wildcard ${MCCOLE}/bin/*.py)
LIB_PY := $(wildcard ${MCCOLE}/extensions/*.py)
EXAMPLES := $(patsubst %/Makefile,%,$(wildcard ${ROOT}/src/*/Makefile))
GITHUB_PAGES := ${ROOT}/CODE_OF_CONDUCT.md ${ROOT}/CONTRIBUTING.md ${ROOT}/LICENSE.md ${ROOT}/README.md
HTML := ${ROOT}/info/head.html ${ROOT}/info/foot.html
INFO := ${ROOT}/info/bibliography.bib ${ROOT}/info/credits.yml ${ROOT}/info/glossary.yml ${ROOT}/info/links.yml
IVY :=  $(wildcard ${MCCOLE}/extensions/*.*) $(wildcard ${MCCOLE}/resources/*.*) $(wildcard ${MCCOLE}/templates/*.*)
TEX := ${ROOT}/info/head.tex ${ROOT}/info/foot.tex
TEX_COPY := ${ROOT}/info/krantz.cls ${ROOT}/info/dedication.tex
PAGES := $(wildcard ${ROOT}/src/*.md) $(wildcard ${ROOT}/src/*/index.md)
SLIDES := $(wildcard ${ROOT}/src/*/slides.html)
SRC_SVG := $(wildcard ${ROOT}/src/*/*.svg)

# Calculated variables.
DOCS := $(patsubst ${ROOT}/src/%.md,${ROOT}/docs/%.html,$(PAGES)) $(patsubst ${ROOT}/src/%/slides.html,${ROOT}/docs/%/slides/index.html,$(SLIDES))
FIG_PDF := $(patsubst ${ROOT}/src/%.svg,${ROOT}/docs/%.pdf,${FIG_SVG})
SRC_PDF := $(patsubst ${ROOT}/src/%.svg,${ROOT}/src/%.pdf,${SRC_SVG})
DOCS_PDF := $(patsubst ${ROOT}/src/%.pdf,${ROOT}/docs/%.pdf,${SRC_PDF})
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
build: ${ROOT}/docs/index.html
${ROOT}/docs/index.html: ${SRC} ${SRC_SVG} ${INFO} ${IVY} ${ROOT}/config.py
	ivy build && touch $@

## serve: build site and run server
.PHONY: serve
serve:
	ivy watch --port ${PORT}

## pdf: create PDF version of material
pdf: ${ROOT}/docs/${STEM}.tex ${DOCS_PDF}
	cp ${ROOT}/info/bibliography.bib ${ROOT}/docs
	cd ${ROOT}/docs && pdflatex ${STEM}
	cd ${ROOT}/docs && biber ${STEM}
	cd ${ROOT}/docs && makeindex ${STEM}
	cd ${ROOT}/docs && pdflatex ${STEM}
	cd ${ROOT}/docs && pdflatex ${STEM}

## ---: ---

## lint: check project structure
.PHONY: lint
lint: clean build
	@python ${MCCOLE}/bin/lint.py \
	--config ${ROOT}/config.py \
	--dom ${MCCOLE}/dom.yml

## inclusions: compare inclusions in prose and slides
.PHONY: inclusions
inclusions:
	@python ${MCCOLE}/bin/compare_inclusions.py --pages ${CHAPTERS}

## examples: re-run examples
.PHONY: examples
examples:
	@for d in ${EXAMPLES}; do echo ""; echo $$d; make -C $$d; done

## fonts: check fonts in diagrams
.PHONY: fonts
fonts:
	@python ${MCCOLE}/bin/check_svg_fonts.py $(SRC_SVG)

## spelling: check spelling against known words
.PHONY: spelling
spelling:
	@make wordlist \
	| python ${MCCOLE}/bin/post_spellcheck.py ${ROOT}/info/wordlist.txt

## wordlist: make a list of unknown and unused words
.PHONY: wordlist
wordlist: ${ROOT}/docs/index.html
	@python ${MCCOLE}/bin/pre_spellcheck.py --pages ${PAGES} --slides ${SLIDES} \
	| aspell -H list \
	| sort \
	| uniq

## ---: ---

## html: create single-page HTML
html: ${ROOT}/docs/all.html
${ROOT}/docs/all.html: ${ROOT}/docs/index.html ${HTML} ${MCCOLE}/bin/make_single_html.py
	python ${MCCOLE}/bin/make_single_html.py \
	--head ${ROOT}/info/head.html \
	--foot ${ROOT}/info/foot.html \
	--root ${ROOT}/docs \
	--title ${TITLE} \
	--tagline "$$(python ${CONFIG} --tagline)" \
	> ${ROOT}/docs/all.html

## latex: create LaTeX document
latex: ${ROOT}/docs/${STEM}.tex
${ROOT}/docs/${STEM}.tex: ${ROOT}/docs/all.html ${MCCOLE}/bin/html_to_latex.py ${CONFIG} ${TEX} ${TEX_COPY}
	python ${MCCOLE}/bin/html_to_latex.py \
	--head ${ROOT}/info/head.tex \
	--foot ${ROOT}/info/foot.tex \
	< ${ROOT}/docs/all.html \
	> ${ROOT}/docs/${STEM}.tex
	python ${CONFIG} --latex > ${ROOT}/docs/config.tex
	cp ${TEX_COPY} ${ROOT}/docs

## pdf-once: create PDF document with a single compilation
pdf-once: ${ROOT}/docs/${STEM}.tex ${DOCS_PDF}
	cd ${ROOT}/docs && pdflatex ${STEM}

## diagrams: convert diagrams from SVG to PDF
diagrams: ${DOCS_PDF}
${ROOT}/src/%.pdf: ${ROOT}/src/%.svg
	${MCCOLE}/bin/convert_drawio.sh $< $@
${ROOT}/docs/%.pdf: ${ROOT}/src/%.pdf
	cp $< $@

## ---: ---

## github: make root pages for GitHub
.PHONY: github
github: ${GITHUB_PAGES}

${ROOT}/CODE_OF_CONDUCT.md: src/conduct/index.md ${MCCOLE}/bin/githubify.py
	python ${MCCOLE}/bin/githubify.py --links ${ROOT}/info/links.yml --title "Code of Conduct" < $< > $@

${ROOT}/CONTRIBUTING.md: src/contrib/index.md ${MCCOLE}/bin/githubify.py
	python ${MCCOLE}/bin/githubify.py --links ${ROOT}/info/links.yml --title "Contributing" < $< > $@

${ROOT}/LICENSE.md: src/license/index.md ${MCCOLE}/bin/githubify.py
	python ${MCCOLE}/bin/githubify.py --links ${ROOT}/info/links.yml --title "License" < $< > $@

${ROOT}/README.md: src/index.md ${MCCOLE}/bin/githubify.py
	python ${MCCOLE}/bin/githubify.py --links ${ROOT}/info/links.yml --title "${TITLE}" < $< > $@

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
	python ${MCCOLE}/bin/run_profile.py

## clean: clean up stray files
clean:
	@find ${ROOT} -name '*~' -exec rm {} \;
	@find ${ROOT} -name '*.bkp' -exec rm {} \;
	@find ${ROOT} -name '.*.dtmp' -exec rm {} \;
	@find ${ROOT} -type d -name __pycache__ | xargs rm -r
	@rm -f \
	${ROOT}/docs/*.aux \
	${ROOT}/docs/*.bbl \
	${ROOT}/docs/*.bcf \
	${ROOT}/docs/*.blg \
	${ROOT}/docs/*.idx \
	${ROOT}/docs/*.ilg \
	${ROOT}/docs/*.ind \
	${ROOT}/docs/*.log \
	${ROOT}/docs/*.out \
	${ROOT}/docs/*.pdf \
	${ROOT}/docs/*.run.xml \
	${ROOT}/docs/*.tex \
	${ROOT}/docs/*.toc

## ---: ---

## status: status of chapters
.PHONY: status
status:
	@python ${MCCOLE}/bin/status.py --config ${ROOT}/config.py --readme ${ROOT}/README.md
	@python ${MCCOLE}/bin/check_prose_slides.py --config ${ROOT}/config.py

## valid: run html5validator on generated files
.PHONY: valid
valid: ${ROOT}/docs/all.html
	@html5validator --root ${ROOT}/docs ${DOCS} \
	--ignore \
	'Attribute "ix-key" not allowed on element "span"' \
	'Attribute "ix-ref" not allowed on element "a"' \
	'Attribute "markdown" not allowed on element'

## vars: show variables
.PHONY: vars
vars:
	@echo ABBREV: ${ABBREV}
	@echo BUILD_DATE: ${BUILD_DATE}
	@echo DOCS: ${DOCS}
	@echo DOCS_PDF: ${DOCS_PDF}
	@echo EXPORT_FILES: ${EXPORT_FILES}
	@echo GITHUB_PAGES: ${GITHUB_PAGES}
	@echo HTML: ${HTML}
	@echo INFO: ${INFO}
	@echo IVY: ${IVY}
	@echo MCCOLE: ${MCCOLE}
	@echo SRC: ${SRC}
	@echo SRC_PDF: ${SRC_PDF}
	@echo SRC_SVG: ${SRC_SVG}
	@echo STEM: ${STEM}
	@echo ROOT: ${ROOT}
	@echo TEX: ${TEX}
	@echo TITLE: ${TITLE}
