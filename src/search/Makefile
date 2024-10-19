# mutate

include ../../examples.mk

BIB_DIR := ${DATA}/bib
TF_IDF_FILE := ${DATA}/tf-idf.csv

## index: make index
index:
	python make_index.py --bibdir ${BIB_DIR} --outfile ${TF_IDF_FILE}

settings: _settings
	@echo "BIB_DIR:" ${BIB_DIR}
	@echo "TF_IDF_FILE:" ${TF_IDF_FILE}
