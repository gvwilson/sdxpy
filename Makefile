.PHONY: commands site serve check bib clean pdf

BIB=bibliography/references.bib
BIN=mccole
DOCS=docs
LUA=pandoc lua
LINKS=mccole/links.md
GLOSSARY=glossary/index.qmd
MD_SRC=$(wildcard *.qmd) $(wildcard */*.qmd)
QUARTO=quarto
SLIDES_SRC=$(wildcard slides.qmd) $(wildcard */slides.qmd)
SLIDES_DST=$(patsubst %.qmd,${DOCS}/%.html,${SLIDES_SRC})
SLIDES_FLAGS=\
  -f markdown \
  -t revealjs \
  -s \
  -V theme=simple \
  -V slideNumber=true \
  --css=mccole/slides.css \
  --lua-filter=mccole/inc-pandoc.lua

## commands: show available commands (*)
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## site: render HTML with Quarto
site:
	${QUARTO} render --to html
	@mkdir -p ${DOCS}/mccole
	@cp mccole/book.css ${DOCS}/mccole
	touch ${DOCS}/.nojekyll

## pdf: render PDF with Quarto
pdf:
	mkdir -p pdf
	${QUARTO} render --to pdf --output-dir=pdf

## serve: preview the site locally
serve:
	${QUARTO} preview

## publish: publish the site
publish:
	${LUA} ${BIN}/publish.lua docs ${OUT} ${EXTRA}

## slides: rebuild just the slides
slides: ${SLIDES_DST}

${DOCS}/%.html: %.qmd
	@mkdir -p $(@D)
	pandoc $< ${SLIDES_FLAGS} -o $@
	@mkdir -p ${DOCS}/mccole
	@cp mccole/slides.css ${DOCS}/mccole/slides.css
	@sed -i '' '/simple\.css/d' $@
	@sed -i '' 's:mccole/slides.css:../mccole/slides.css:g' $@

## check: check structure, spelling, etc.
check: check-bib check-links check-glossary check-typos

## check-bib: check bibliography
check-bib:
	@${LUA} ${BIN}/check-bib.lua ${BIB} ${MD_SRC}

## check-links: check Markdown links
check-links:
	@${LUA} ${BIN}/check-links.lua ${LINKS} ${MD_SRC}

## check-glossary: check glossary references
check-glossary:
	@${LUA} ${BIN}/check-glossary.lua ${GLOSSARY} ${MD_SRC}

## check-typos: check spelling
check-typos:
	@typos -c mccole/typos.toml ${MD_SRC} ${SLIDES_SRC}

## clean: remove generated and cache files
clean:
	rm -rf .quarto _book
	find . -type f -name '*~' -delete
