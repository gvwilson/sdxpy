all: commands

## commands: show available commands (*)
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## check: check code issues
check:
	@ruff check .

## clean: clean up
clean:
	@rm -rf ./dist
	@find . -path ./.venv -prune -o -type d -name __pycache__ -exec rm -rf {} +
	@find . -path ./.venv -prune -o -type d -name .ruff_cache -exec rm -rf {} +
	@find . -path ./.venv -prune -o -type f -name '*~' -exec rm {} +

## fix: fix code issues
fix:
	@ruff check --fix ${LESSONS}

## format: format code
format:
	@ruff format ${LESSONS}

## html: check HTML
html:
	@mccole check --src . --dst docs

## lint: run all code checks
lint:
	@make check
	@make types

## site: build documentation
site:
	@mccole build --math --src . --dst docs
	@touch docs/.nojekyll

## serve: serve documentation
serve:
	python -m http.server -d docs

## examples: regenerate example output
examples: ${EXAMPLES_OUT}

%.txt: %.py
	python $< ${SEED} > $@
