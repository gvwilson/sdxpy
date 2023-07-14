#!/usr/bin/env bash
# Create PDF versions of slides
for slug in $*
do
    mkdir -p ./slides/${slug}
    decktape remark https://third-bit.com/sdxpy/${slug}/slides/index.html ./slides/${slug}/slides.pdf
done
