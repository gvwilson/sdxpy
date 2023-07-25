#!/usr/bin/env bash
# Create PDF versions of slides
OUTPUT_DIR=/tmp/sdxpy-slides
mkdir -p ${OUTPUT_DIR}
for slug in $*
do
    decktape remark http://localhost:4000/${slug}/slides/index.html ${OUTPUT_DIR}/${slug}/slides.pdf
done
