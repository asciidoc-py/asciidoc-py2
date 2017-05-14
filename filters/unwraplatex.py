#!/usr/bin/env python2
'''
NAME
    unwraplatex - Removes delimiters from LaTeX source text

SYNOPSIS
    latex2img STDIN

DESCRIPTION
    This filter reads LaTeX source text from STDIN and removes the
    surrounding \[ and \] delimiters.
'''

import re, sys

sys.stdout.write(re.sub("(?s)\A(?:\\\\\[\s*)?(.*?)(?:\\\\\])?\Z", "\\1", sys.stdin.read().rstrip()))
# NOTE append endline in result to prevent 'no output from filter' warning
sys.stdout.write("\n")
