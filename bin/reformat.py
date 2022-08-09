#!/usr/bin/env python

'''Wrap long lines and do other cleanup for code output.'''

import os
import re
import sys

import utils

# Strip out file protocol.
PROTOCOL = 'file://'

# Home directory replacement.
HERE = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
FAKE = '/u/stjs'

# How to show removed lines. (Can't use literal ellipsis '…' because it confuses LaTeX.)
REMOVED = '...'

# Output slice size.
SLICE = 10

# Pattern for leading indentation.
INDENT = re.compile(r'^(\s+)')


def reformat(options):
    '''Main driver.'''
    lines = [x.rstrip() for x in sys.stdin.read().rstrip().split('\n')]
    selected = select(options, lines)
    wrapped = wrap(options, selected)
    for line in wrapped:
        print(line)


def select(options, lines):
    '''Select desired lines vertically.'''
    if options.slice:
        return lines[:SLICE] + [REMOVED] + lines[-SLICE:]
    return lines


def wrap(options, lines):
    '''Wrap lines.'''
    result = []
    for line in lines:
        line = line.replace(PROTOCOL, '').replace(HERE, FAKE)
        if len(line) == 0:
            result.append(line)
            continue
        match = INDENT.match(line)
        indent = match.group(1) if match else ''
        while len(line) > 0:
            front, line, terminator = split(line)
            result.append(f'{front}{terminator}')
            if len(line) > 0:
                line = indent + line.lstrip()
    return result


def split(line):
    '''Split a line.'''
    if len(line) <= utils.WIDTH:
        return line, '', ''
    for i in range(utils.WIDTH, 0, -1):
        if (line[i] == ' '):
            return line[:i], line[i:], ' \\'
    return line[:utils.WIDTH], line[utils.WIDTH:], ' \\'


if __name__ == '__main__':
    options = utils.get_options(
        ['--slice', None, 'Take slice out of input?']
    )
    reformat(options)
