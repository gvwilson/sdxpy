#!/usr/bin/env bash
if grep -q diagrams.net $1
then
    draw.io --export --crop --output $2 $1
fi
