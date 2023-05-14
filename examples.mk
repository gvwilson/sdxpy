# Get the path to this file from wherever it is included.
# See https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
RULES_PATH:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# How to reformat output.
COLUMNS=68
REFORMAT:=python ${RULES_PATH}bin/reformat.py --home /sd4ds --columns ${COLUMNS}

# The including file must define a variable TARGETS with the names of everything
# to be created.
all: ${TARGETS}

# Show the targets defined by the including file.
targets:
	@echo ${TARGETS}

# Create HTML or text from a shell script that runs some Python.
# Normally used when there are parameters to the Python file but no extra
# dependencies.
%.html: %.sh %.py
	bash $< 2>&1 | ${REFORMAT} > $@
%.out: %.sh %.py
	bash $< 2>&1 | ${REFORMAT} > $@

# Create HTML or text when there is only a shell script.
# Normally used when the output depends on multiple .py files, in which case the
# including file must define dependencies.
%.html: %.sh
	bash $< 2>&1 | ${REFORMAT} > $@
%.out: %.sh
	bash $< 2>&1 | ${REFORMAT} > $@

# Create HTML or text by running Python without parameters.
%.html: %.py
	python $< 2>&1 | ${REFORMAT} > $@
%.out: %.py
	python $< 2>&1 | ${REFORMAT} > $@

# Get rid of all generated files.
erase:
	rm -f ${TARGETS}
