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
ARK :=  $(wildcard ${MCCOLE}/extensions/*.py) $(wildcard ${MCCOLE}/resources/*.*) $(wildcard ${MCCOLE}/templates/*.*)
BIN_PY := $(wildcard ${MCCOLE}/bin/*.py)
COMBINED_HTML := ${ROOT}/docs/all.html
DOCS_INDEX := ${ROOT}/docs/index.html
EXAMPLES := $(patsubst %/Makefile,%,$(wildcard ${ROOT}/src/*/Makefile))
GITHUB_PAGES := ${ROOT}/CODE_OF_CONDUCT.md ${ROOT}/CONTRIBUTING.md ${ROOT}/LICENSE.md ${ROOT}/README.md
HTML_COPY := ${ROOT}/info/head.html ${ROOT}/info/foot.html
LIB_PY := $(wildcard ${MCCOLE}/extensions/*.py)
SRC_PAGES := $(wildcard ${ROOT}/src/*.md) $(wildcard ${ROOT}/src/*/index.md)
SRC_SLIDES := $(wildcard ${ROOT}/src/*/slides.html)
SRC_SVG := $(wildcard ${ROOT}/src/*/*.svg)
TEX_COPY := ${ROOT}/info/krantz.cls ${ROOT}/info/dedication.tex
TEX_FILES := ${ROOT}/info/head.tex ${ROOT}/info/foot.tex

INFO_BIB := ${ROOT}/info/bibliography.bib
INFO_GLOSSARY := ${ROOT}/info/glossary.yml
INFO_LINKS := ${ROOT}/info/links.yml
INFO_FILES := ${INFO_BIB} ${ROOT}/info/credits.yml ${INFO_GLOSSARY} ${INFO_LINKS}

# Calculated variables.
DOCS := ${DOCS_PAGES} ${DOCS_SLIDES}
DOCS_PAGES := $(patsubst ${ROOT}/src/%.md,${ROOT}/docs/%.html,$(SRC_PAGES))
SRC_PDF := $(patsubst ${ROOT}/src/%.svg,${ROOT}/src/%.pdf,${SRC_SVG})
DOCS_PDF := $(patsubst ${ROOT}/src/%.pdf,${ROOT}/docs/%.pdf,${SRC_PDF})
DOCS_SLIDES := $(patsubst ${ROOT}/src/%/slides.html,${ROOT}/docs/%/slides/index.html,$(SRC_SLIDES))
FIG_PDF := $(patsubst ${ROOT}/src/%.svg,${ROOT}/docs/%.pdf,${FIG_SVG})
SRC := ${SRC_PAGES} ${SRC_SLIDES}
STEM := ${ABBREV}-${BUILD_DATE}

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
build: ${DOCS_INDEX}
${DOCS_INDEX}: ${SRC} ${SRC_SVG} ${INFO_FILES} ${ARK} ${ROOT}/config.py
	ark build && touch $@

## serve: build site and run server
.PHONY: serve
serve:
	ark watch --port ${PORT}

## pdf: create PDF version of material
pdf: ${ROOT}/docs/${STEM}.tex ${INFO_BIB} ${DOCS_PDF}
	cp ${INFO_BIB} ${ROOT}/docs
	cd ${ROOT}/docs && pdflatex ${STEM}
	cd ${ROOT}/docs && biber ${STEM}
	cd ${ROOT}/docs && makeindex ${STEM}
	cd ${ROOT}/docs && pdflatex ${STEM}
	cd ${ROOT}/docs && pdflatex ${STEM}

## ---: ---

## lint: check project structure
.PHONY: lint
BIN_LINT := ${MCCOLE}/bin/lint.py
lint: ${DOCS_INDEX} ${BIN_LINT}
	@python ${BIN_LINT} \
	--config ${ROOT}/config.py \
	--dom ${MCCOLE}/dom.yml \
	--pages ${DOCS_PAGES}

## headings: show problematic headings (many false positives)
.PHONY: headings
BIN_CHECK_HEADINGS := ${MCCOLE}/bin/check_headings.py
headings:
	@python ${BIN_CHECK_HEADINGS} --config ${ROOT}/config.py

## inclusions: compare inclusions in prose and slides
.PHONY: inclusions
BIN_COMPARE_INCLUSIONS := ${MCCOLE}/bin/compare_inclusions.py 
inclusions:
	@python ${BIN_COMPARE_INCLUSIONS} --chapters ${CHAPTERS}

## examples: re-run examples
.PHONY: examples
examples:
	@for d in ${EXAMPLES}; do echo ""; echo $$d; make -C $$d; done

## check-examples: check which examples would re-run
check-make:
	@for d in ${EXAMPLES}; do echo ""; echo $$d; make -C $$d --dry-run; done

## fonts: check fonts in diagrams
.PHONY: fonts
BIN_CHECK_FONTS := ${MCCOLE}/bin/check_svg_fonts.py
fonts:
	@python ${BIN_CHECK_FONTS} $(SRC_SVG)

## spelling: check spelling against known words
.PHONY: spelling
BIN_SPELLING := ${MCCOLE}/bin/spelling.py
spelling: ${DOCS_INDEX} ${BIN_SPELLING}
	@python ${BIN_SPELLING} --config ${ROOT}/config.py --extra info/wordlist.txt

## index: show all index entries
.PHONY: index
BIN_SHOW_INDEX := ${MCCOLE}/bin/show_index.py 
index: ${DOCS_INDEX} ${BIN_SHOW_INDEX}
	@python ${BIN_SHOW_INDEX} --config ${CONFIG}

## ---: ---

## html: create single-page HTML
html: ${COMBINED_HTML}
BIN_MAKE_SINGLE_HTML :=  ${MCCOLE}/bin/make_single_html.py
${COMBINED_HTML}: ${DOCS_INDEX} ${HTML_COPY} ${BIN_MAKE_SINGLE_HTML}
	python ${BIN_MAKE_SINGLE_HTML} \
	--head ${ROOT}/info/head.html \
	--foot ${ROOT}/info/foot.html \
	--root ${ROOT}/docs \
	--title "${TITLE}" \
	--tagline "$$(python ${CONFIG} --tagline)" \
	> ${COMBINED_HTML}

## latex: create LaTeX document
latex: ${ROOT}/docs/${STEM}.tex
BIN_HTML_TO_LATEX :=  ${MCCOLE}/bin/html_to_latex.py
${ROOT}/docs/${STEM}.tex: ${COMBINED_HTML} ${TEX_FILES} ${TEX_COPY} ${INFO_GLOSSARY} ${BIN_HTML_TO_LATEX}
	python ${BIN_HTML_TO_LATEX} \
	--head ${ROOT}/info/head.tex \
	--foot ${ROOT}/info/foot.tex \
	--glossary ${INFO_GLOSSARY} \
	--language ${LANG} \
	< ${COMBINED_HTML} \
	> ${ROOT}/docs/${STEM}.tex
	python ${CONFIG} --latex > ${ROOT}/docs/config.tex
	cp ${TEX_COPY} ${ROOT}/docs

## pdf-once: create PDF document with a single compilation
pdf-once: ${ROOT}/docs/${STEM}.tex ${DOCS_PDF}
	cd ${ROOT}/docs && pdflatex ${STEM}

ifdef SYLLABUS_DIR
## syllabus: remake syllabus diagrams
BIN_MAKE_DOT := ${MCCOLE}/bin/make_dot.py
SYLLABUS_DEPS := ${CONFIG} $(patsubst %,${ROOT}/src/%/index.md,${CHAPTERS}) ${MCCOLE}/bin/make_dot.py
SYLLABUS_FILES := $(patsubst %,${SYLLABUS_DIR}/syllabus%,_regular.pdf _regular.svg _linear.pdf _linear.svg)

syllabus: ${SYLLABUS_FILES}

${SYLLABUS_DIR}/syllabus_%.pdf: ${ROOT}/info/%.dot
	dot -Tpdf $< > $@

${SYLLABUS_DIR}/syllabus_%.svg: ${ROOT}/info/%.dot
	dot -Tsvg $< > $@

${ROOT}/info/regular.dot: ${SYLLABUS_DEPS} ${BIN_MAKE_DOT}
	@python ${BIN_MAKE_DOT} --config ${CONFIG} --kind regular --skip intro finale --output $@

${ROOT}/info/linear.dot: ${SYLLABUS_DEPS} ${BIN_MAKE_DOT}
	@python ${BIN_MAKE_DOT} --config ${CONFIG} --kind linear --skip intro finale --output $@
endif

## diagrams: convert diagrams from SVG to PDF
diagrams: ${DOCS_PDF}
BIN_CONVERT_DRAWIO := ${MCCOLE}/bin/convert_drawio.sh
${ROOT}/src/%.pdf: ${ROOT}/src/%.svg ${BIN_CONVERT_DRAWIO}
	${BIN_CONVERT_DRAWIO} $< $@
${ROOT}/docs/%.pdf: ${ROOT}/src/%.pdf
	cp $< $@

## ---: ---

## github: make root pages for GitHub
.PHONY: github
BIN_MAKE_GITHUB_PAGE := ${MCCOLE}/bin/make_github_page.py
github: ${GITHUB_PAGES}

${ROOT}/CODE_OF_CONDUCT.md: src/conduct/index.md ${BIN_MAKE_GITHUB_PAGE}
	python ${BIN_MAKE_GITHUB_PAGE} --links ${INFO_LINKS} --title "Code of Conduct" < $< > $@

${ROOT}/CONTRIBUTING.md: src/contrib/index.md ${ROOT}/info/contrib.md ${BIN_MAKE_GITHUB_PAGE}
	python ${BIN_MAKE_GITHUB_PAGE} --append ${ROOT}/info/contrib.md --links ${INFO_LINKS} --title "Contributing" < $< > $@

${ROOT}/LICENSE.md: src/license/index.md ${BIN_MAKE_GITHUB_PAGE}
	python ${BIN_MAKE_GITHUB_PAGE} --links ${INFO_LINKS} --title "License" < $< > $@

${ROOT}/README.md: src/index.md ${BIN_MAKE_GITHUB_PAGE}
	python ${BIN_MAKE_GITHUB_PAGE} --links ${INFO_LINKS} --title "${TITLE}" < $< > $@

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
BIN_RUN_PROFILE := ${MCCOLE}/bin/run_profile.py
profile:
	python ${BIN_RUN_PROFILE}

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
BIN_STATUS := ${MCCOLE}/bin/status.py
status: ${DOCS_INDEX} ${BIN_STATUS}
	@python ${BIN_STATUS} --highlight ascii --config ${ROOT}/config.py

## valid: run html5validator on generated files
.PHONY: valid
valid: ${COMBINED_HTML}
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
