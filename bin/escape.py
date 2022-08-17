#!/usr/bin/env python

"""Transform input text to escaped HTML."""

import html
import sys

text = sys.stdin.read()
text = html.escape(text)
sys.stdout.write(text)
