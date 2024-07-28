# ----------------------------------------------------------------------
# Generic McCole Makefile
# ----------------------------------------------------------------------

# By default, show available commands (by finding '##' comments)
.DEFAULT: commands

# LaTeX engines
LATEX=xelatex
BIBTEX=biber
MAKEINDEX=makeindex

# Project root directory
ROOT := .

# Project theme
THEME := $(shell python ${ROOT}/config.py)

# Where to find tools
THEME_BIN := ${ROOT}/lib/${THEME}/bin

# LaTeX auxiliary files
LATEX_FILES := $(wildcard ${ROOT}/lib/${THEME}/latex/*.*)

# Standard GitHub pages (in root directory rather than website source directory)
GITHUB_PAGES := ${ROOT}/CODE_OF_CONDUCT.md ${ROOT}/LICENSE.md

# Information files
INFO_GLOSSARY := ${ROOT}/info/glossary.yml
INFO_BIB := info/bibliography.bib
TMP_BIB := tmp/bibliography.html

# All Markdown source pages
SRC_PAGES := $(wildcard ${ROOT}/src/*.md) $(wildcard ${ROOT}/src/*/index.md)

# Generated HTML pages
DOCS_PAGES := $(patsubst ${ROOT}/src/%.md,${ROOT}/docs/%.html,$(SRC_PAGES))

# Generated LaTeX file
LATEX_PAGE := ${ROOT}/docs/${THEME}.tex

# All SVG diagrams
SRC_SVG := $(wildcard ${ROOT}/src/*/*.svg)
SVG_WIDTH := 640

# Generated PDFs
SRC_PDF := $(patsubst ${ROOT}/src/%.svg,${ROOT}/src/%.pdf,${SRC_SVG})
DOCS_PDF := $(patsubst ${ROOT}/src/%.pdf,${ROOT}/docs/%.pdf,${SRC_PDF})

# Keep the PDF versions of diagrams under the 'src' directory between builds
.PRECIOUS: ${SRC_PDF}

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## build: rebuild site without running server
.PHONY: build
build: ${TMP_BIB}
	ark build
	@touch ${ROOT}/docs/.nojekyll

## serve: build site and run server
.PHONY: serve
serve: ${TMP_BIB}
	ark watch

## latex: regenerate LaTeX file
latex: ${LATEX_PAGE}
${LATEX_PAGE}: ${DOCS_PAGES} ${THEME_BIN}/latex.py ${LATEX_FILES}
	@python ${THEME_BIN}/latex.py --root ${ROOT} > ${LATEX_PAGE}

## pdf: create PDF version of material
pdf: ${LATEX_PAGE} ${INFO_BIB} ${DOCS_PDF}
	cp ${INFO_BIB} ${ROOT}/docs
	cp ${ROOT}/lib/${THEME}/latex/krantz.cls ${ROOT}/docs
	rm -f ${ROOT}/docs/${THEME}.idx ${ROOT}/docs/${THEME}.ind
	cd ${ROOT}/docs && ${LATEX} ${THEME}
	cd ${ROOT}/docs && ${BIBTEX} ${THEME}
	cd ${ROOT}/docs && ${MAKEINDEX} ${THEME}
	cd ${ROOT}/docs && ${LATEX} ${THEME}
	cd ${ROOT}/docs && ${LATEX} ${THEME}

## diagrams: convert diagrams from SVG to PDF
diagrams: ${DOCS_PDF}
${ROOT}/src/%.pdf: ${ROOT}/src/%.svg ${THEME_BIN}/convert_drawio.sh
	bash ${THEME_BIN}/convert_drawio.sh $< $@
${ROOT}/docs/%.pdf: ${ROOT}/src/%.pdf
	cp $< $@

## profile: profile compilation
.PHONY: profile
profile:
	python ${THEME_BIN}/run_profile.py

## bib: rebuild HTML version of bibliography
bib: ${TMP_BIB} ${THEME_BIN}/make_bibliography.py
${TMP_BIB}: ${INFO_BIB}
	@mkdir -p ${ROOT}/tmp
	python ${THEME_BIN}/make_bibliography.py --infile $< --outfile $@

## lint: check project
.PHONY: lint
lint:
	@make lint_theme
	@make lint_svg
	@make lint_html

## lint_theme: check theme aspects of project
.PHONY: lint_theme
lint_theme:
	@python ${THEME_BIN}/lint.py \
	--dom ${ROOT}/lib/mccole/dom.yml \
	--exclude Makefile slides.html \
	--htmldir ${ROOT}/docs \
	--root ${ROOT} \
	--skipslides

## lint_svg: check diagrams
.PHONY: lint_svg
lint_svg:
	@python ${THEME_BIN}/lint_svg.py ${FONT_FAMILY} ${FONT_SIZE} \
	--width ${SVG_WIDTH} \
	--files ${SRC_SVG}

## lint_html: check HTML validity
.PHONY: lint_html
lint_html:
	@html5validator --root ${ROOT}/docs ${DOCS_PAGES} \
	--ignore \
	'Attribute "ix-key" not allowed on element "span"' \
	'Attribute "ix-ref" not allowed on element "a"' \
	'Attribute "markdown" not allowed on element "a"' \
	'Attribute "markdown" not allowed on element "div"' \
	'Attribute "markdown" not allowed on element "span"' \
	'Attribute "markdown" not allowed on element "td"'

## style: check Python code style
.PHONY: style
style:
	@ruff check .

## reformat: reformat unstylish Python code
.PHONY: reformat
reformat:
	@ruff format .

## pack: create a release
.PHONY: pack
pack:
	@rm -f mccole.zip
	zip -r mccole.zip \
	CODE_OF_CONDUCT.md \
	LICENSE.md \
	docs/.nojekyll \
	lib \
	src/bib \
	src/colophon \
	src/conduct \
	src/contents \
	src/contrib \
	src/glossary \
	src/license \
	-x '**/__pycache__/*' -x '*~'

## unpack: make required files after unzipping mccole.zip
.PHONY: unpack
unpack:
	mkdir -p info src
	touch \
	config.py \
	Makefile \
	CODE_OF_CONDUCT.md \
	CONTRIBUTING.md \
	LICENSE.md \
	README.md \
	requirements.txt \
	info/bibliography.bib \
	info/glossary.yml \
	info/links.yml \
	info/thanks.yml \
	src/index.md

## clean: clean up stray files
.PHONY: clean
clean:
	@find ${ROOT} -name '*~' -exec rm {} \;
	@find ${ROOT} -name '*.bkp' -exec rm {} \;
	@find ${ROOT} -name '.*.dtmp' -exec rm {} \;
	@find ${ROOT} -type d -name __pycache__ | xargs rm -r
	@find ${ROOT} -type d -name .pytest_cache | xargs rm -r
