# Shared build targets for Mccole Quarto projects.
# Include in the project's Makefile with:
#
#     include mccole/mccole.mk

.PHONY: commands site serve check bib clean pdf update-mccole

BIB ?= bibliography/references.bib
BIN = mccole
DOCS = docs
LUA = pandoc lua
LINKS ?= config/links.md
GLOSSARY ?= glossary/index.qmd
QUARTO = quarto
TYPOS_CONFIG ?= config/typos.toml
SLIDES_EXTRA ?=

PAGES_SRC = $(wildcard *.qmd) $(wildcard */*.qmd)
PAGES_DST = $(patsubst %.qmd,$(DOCS)/%.html,$(PAGES_SRC))
SLIDES_SRC = $(wildcard slides.qmd) $(wildcard */slides.qmd)
SLIDES_DST = $(patsubst %.qmd,$(DOCS)/%.html,$(SLIDES_SRC))
SLIDES_FLAGS = \
  -f markdown \
  -t revealjs \
  -s \
  -V theme=simple \
  -V slideNumber=true \
  --css=mccole/mccole-slides.css \
  --mathjax \
  --syntax-highlighting=tango \
  --lua-filter=mccole/inc-pandoc.lua \
  $(SLIDES_EXTRA)

## commands: show available commands (*)
commands:
	@grep -h -E '^##' $(MAKEFILE_LIST) \
	| sed -e 's/## //g' \
	| column -t -s ':'

## site: render pages and slides
site:
	$(QUARTO) render --to html
	@$(MAKE) slides
	@mkdir -p $(DOCS)/mccole
	@cp mccole/mccole-slides.css $(DOCS)/mccole/mccole-slides.css
	@cp mccole/forma.js $(DOCS)/mccole/forma.js
	@cp mccole/mccole-forma.css $(DOCS)/mccole/mccole-forma.css
	@if [ -d images ]; then cp -r images $(DOCS)/images; fi
	@touch $(DOCS)/.nojekyll

## pdf: generate PDF
pdf:
	mkdir -p pdf
	$(QUARTO) render --to pdf --output-dir=pdf

## serve: preview the site locally
serve:
	$(QUARTO) preview

## publish: publish the site
publish:
	$(LUA) $(BIN)/publish.lua docs $(OUT) $(EXTRA)

## update-mccole: refresh mccole/ from the mcq remote
update-mccole:
	git fetch mcq
	rm -rf mccole
	git checkout mcq/main -- mccole

## slides: rebuild the slides using Pandoc
slides: $(SLIDES_DST)

$(DOCS)/%.html: %.qmd
	@mkdir -p $(@D)
	pandoc $< $(SLIDES_FLAGS) -o $@
	@mkdir -p $(DOCS)/mccole
	@cp mccole/mccole-slides.css $(DOCS)/mccole/mccole-slides.css
	@sed -i '' '/simple\.css/d' $@
	@sed -i '' 's:mccole/mccole-slides.css:../mccole/mccole-slides.css:g' $@

## check: check structure, spelling, etc.
check: check-bib check-links check-glossary check-formatting check-typos check-html

## check-bib: check bibliography
check-bib:
	@-$(LUA) $(BIN)/check-bib.lua $(BIB) $(PAGES_SRC)

## check-links: check Markdown links
check-links:
	@-$(LUA) $(BIN)/check-links.lua $(LINKS) $(PAGES_SRC)

## check-glossary: check glossary references
check-glossary:
	@-$(LUA) $(BIN)/check-glossary.lua $(GLOSSARY) $(PAGES_SRC)

## check-formatting: check include formatting
check-formatting:
	@-$(LUA) $(BIN)/check-formatting.lua $(PAGES_SRC)

## check-typos: check spelling
check-typos:
	@-typos -c $(TYPOS_CONFIG) $(PAGES_SRC) $(SLIDES_SRC)

## check-html: check accessibility
check-html:
	@-$(LUA) $(BIN)/check-html.lua $(DOCS)/*.html $(DOCS)/*/*.html

## clean: remove generated and cache files
clean:
	rm -rf .quarto _book
	find . -type f -name '*~' -delete
