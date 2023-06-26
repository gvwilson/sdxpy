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

# Get local configuration from the Ark configuration file.
CONFIG := ${ROOT}/config.py
ABBREV := $(shell python ${CONFIG} --abbrev)
BUILD_DATE := $(shell date '+%Y-%m-%d')
CHAPTERS := $(shell python ${CONFIG} --chapters)
LANG := $(shell python ${CONFIG} --lang)
TITLE := $(shell python ${CONFIG} --title)

# Direct variables.
BIN_PY := $(wildcard ${MCCOLE}/bin/*.py)
LIB_PY := $(wildcard ${MCCOLE}/extensions/*.py)
EXAMPLES := $(patsubst %/Makefile,%,$(wildcard ${ROOT}/src/*/Makefile))
GITHUB_PAGES := ${ROOT}/CODE_OF_CONDUCT.md ${ROOT}/CONTRIBUTING.md ${ROOT}/LICENSE.md ${ROOT}/README.md
HTML_COPY := ${ROOT}/info/head.html ${ROOT}/info/foot.html
INFO_FILES := ${ROOT}/info/bibliography.bib ${ROOT}/info/credits.yml ${ROOT}/info/glossary.yml ${ROOT}/info/links.yml
ARK :=  $(wildcard ${MCCOLE}/extensions/*.py) $(wildcard ${MCCOLE}/resources/*.*) $(wildcard ${MCCOLE}/templates/*.*)
TEX_FILES := ${ROOT}/info/head.tex ${ROOT}/info/foot.tex
TEX_COPY := ${ROOT}/info/krantz.cls ${ROOT}/info/dedication.tex
SRC_PAGES := $(wildcard ${ROOT}/src/*.md) $(wildcard ${ROOT}/src/*/index.md)
SRC_SLIDES := $(wildcard ${ROOT}/src/*/slides.html)
SRC_SVG := $(wildcard ${ROOT}/src/*/*.svg)

# Calculated variables.
STEM := ${ABBREV}-${BUILD_DATE}
SRC := ${SRC_PAGES} ${SRC_SLIDES}
DOCS_PAGES := $(patsubst ${ROOT}/src/%.md,${ROOT}/docs/%.html,$(SRC_PAGES))
DOCS_SLIDES := $(patsubst ${ROOT}/src/%/slides.html,${ROOT}/docs/%/slides/index.html,$(SRC_SLIDES))
DOCS := ${DOCS_PAGES} ${DOCS_SLIDES}
FIG_PDF := $(patsubst ${ROOT}/src/%.svg,${ROOT}/docs/%.pdf,${FIG_SVG})
SRC_PDF := $(patsubst ${ROOT}/src/%.svg,${ROOT}/src/%.pdf,${SRC_SVG})
DOCS_PDF := $(patsubst ${ROOT}/src/%.pdf,${ROOT}/docs/%.pdf,${SRC_PDF})

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
${ROOT}/docs/index.html: ${SRC} ${SRC_SVG} ${INFO_FILES} ${ARK} ${ROOT}/config.py
	ark build && touch $@

## serve: build site and run server
.PHONY: serve
serve:
	ark watch --port ${PORT}

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
	--dom ${MCCOLE}/dom.yml \
	--pages ${DOCS_PAGES}

## inclusions: compare inclusions in prose and slides
.PHONY: inclusions
inclusions:
	@python ${MCCOLE}/bin/compare_inclusions.py --chapters ${CHAPTERS}

## examples: re-run examples
.PHONY: examples
examples:
	@for d in ${EXAMPLES}; do echo ""; echo $$d; make -C $$d; done

## check-make: check Makefiles
check-make:
	@for d in ${EXAMPLES}; do echo ""; echo $$d; make -C $$d --dry-run; done

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
	@python ${MCCOLE}/bin/pre_spellcheck.py --pages ${SRC_PAGES} --slides ${SRC_SLIDES} \
	| aspell -H list \
	| sort \
	| uniq

## ---: ---

## html: create single-page HTML
html: ${ROOT}/docs/all.html
${ROOT}/docs/all.html: ${ROOT}/docs/index.html ${HTML_COPY} ${MCCOLE}/bin/make_single_html.py
	python ${MCCOLE}/bin/make_single_html.py \
	--head ${ROOT}/info/head.html \
	--foot ${ROOT}/info/foot.html \
	--root ${ROOT}/docs \
	--title "${TITLE}" \
	--tagline "$$(python ${CONFIG} --tagline)" \
	> ${ROOT}/docs/all.html

## latex: create LaTeX document
latex: ${ROOT}/docs/${STEM}.tex
${ROOT}/docs/${STEM}.tex: ${ROOT}/docs/all.html ${MCCOLE}/bin/html_to_latex.py ${TEX_FILES} ${TEX_COPY}
	python ${MCCOLE}/bin/html_to_latex.py \
	--head ${ROOT}/info/head.tex \
	--foot ${ROOT}/info/foot.tex \
	--glossary ${ROOT}/info/glossary.yml \
	--language ${LANG} \
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

ifdef SYLLABUS_DIR
## syllabus: remake syllabus diagram
SYLLABUS_IMG=${SYLLABUS_DIR}/syllabus_regular.pdf ${SYLLABUS_DIR}/syllabus_regular.svg ${SYLLABUS_DIR}/syllabus_regular.png ${SYLLABUS_DIR}/syllabus_linear.pdf ${SYLLABUS_DIR}/syllabus_linear.png ${SYLLABUS_DIR}/syllabus_linear.svg
syllabus: ${SYLLABUS_IMG}
${SYLLABUS_IMG}: ${CONFIG} $(patsubst %,${ROOT}/src/%/index.md,${CHAPTERS}) ${MCCOLE}/bin/make_dot.py
	python ${MCCOLE}/bin/make_dot.py --config ${CONFIG} --skip intro finale --output ${SYLLABUS_DIR}/syllabus
	rm -f ${SYLLABUS_DIR}/syllabus_*.gv
endif

## github: make root pages for GitHub
.PHONY: github
github: ${GITHUB_PAGES}

${ROOT}/CODE_OF_CONDUCT.md: src/conduct/index.md ${MCCOLE}/bin/make_github_page.py
	python ${MCCOLE}/bin/make_github_page.py --links ${ROOT}/info/links.yml --title "Code of Conduct" < $< > $@

${ROOT}/CONTRIBUTING.md: src/contrib/index.md ${MCCOLE}/bin/make_github_page.py
	python ${MCCOLE}/bin/make_github_page.py --append ${ROOT}/info/contrib.md --links ${ROOT}/info/links.yml --title "Contributing" < $< > $@

${ROOT}/LICENSE.md: src/license/index.md ${MCCOLE}/bin/make_github_page.py
	python ${MCCOLE}/bin/make_github_page.py --links ${ROOT}/info/links.yml --title "License" < $< > $@

${ROOT}/README.md: src/index.md ${MCCOLE}/bin/make_github_page.py
	python ${MCCOLE}/bin/make_github_page.py --links ${ROOT}/info/links.yml --title "${TITLE}" < $< > $@

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
	@find ${ROOT} -type d -name .pytest_cache | xargs rm -r
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
	@echo ARK: ${ARK}
	@echo BUILD_DATE: ${BUILD_DATE}
	@echo DOCS: ${DOCS}
	@echo DOCS_PDF: ${DOCS_PDF}
	@echo EXPORT_FILES: ${EXPORT_FILES}
	@echo GITHUB_PAGES: ${GITHUB_PAGES}
	@echo HTML_COPY: ${HTML_COPY}
	@echo INFO_FILES: ${INFO_FILES}
	@echo MCCOLE: ${MCCOLE}
	@echo ROOT: ${ROOT}
	@echo SRC: ${SRC}
	@echo SRC_PAGES: ${SRC_PAGES}
	@echo SRC_PDF: ${SRC_PDF}
	@echo SRC_SVG: ${SRC_SVG}
	@echo STEM: ${STEM}
	@echo SYLLABUS_DIR: ${SYLLABUS_DIR}
	@echo SYLLABUS_IMG: ${SYLLABUS_IMG}
	@echo TEX_COPY: ${TEX_COPY}
	@echo TEX_FILES: ${TEX_FILES}
	@echo TITLE: ${TITLE}
